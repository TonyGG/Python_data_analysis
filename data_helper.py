"""
Module for fetching data from postgres in an analytics-friendly manner.

Copyright (c) 2020, Antuit Inc. - All rights reserved
Proprietary and confidential
Unauthorized copying of this file, via any medium, is strictly prohibited.
"""
import datetime
import json
import os
from os.path import join

import pandas as pd
import psycopg2


def stringable(x):
    return isinstance(x, str) or isinstance(x, datetime.datetime)


class DataHelper:
    """
    Data manager with connection and transformation convenience functions.

    Parameters
    ----------
    json_path : str
        Absolute path to a JSON file containing the connection parameters.
    connection_params : dict
        Dictionary of parameters to pass to `psycopg2.connect`.

    Examples
    --------
    The easiest way to use the :class:`Datahelper` is to have a JSON file with
    all the connection parameters ready to go in your `GSK_HOME` directory.

    >>> import json
    >>> import os
    >>> from gsk import DataHelper
    >>> json_path = os.path.join(os.environ['GSK_HOME'], 'connection.json')
    >>> with open(json_path, 'r') as f:
    ...     connection_params = json.load(f)
    >>> connection_params.keys()
    dict_keys(['host', 'port', 'dbname', 'schema', 'user', 'password'])

    A `DataHelper` can be constructed by either giving it the path to this JSON,
    or by passing each of the parameters as a keyword.

    >>> dh = DataHelper(json_path=json_path)
    >>> the_same_dh = DataHelper(connection_params=connection_params)

    The most common use for the `DataHelper` is to get the sales data for a
    given market/category/sub_category.

    >>> au_cleansers = dh.load_market_category('AU', 'ORAL CARE', 'DENTURE CLEANSERS')

    You may also query the database directly using the :class:`DataHelper`.

    >>> dh.query("select distinct vendor_name from test_star.dim_product where brand_name = 'AQUAFRESH'")
           vendor_name
    0  GLAXOSMITHKLINE

    """

    required = {'user', 'password', 'host', 'dbname', 'port'}

    def __init__(self, json_path: str = None, connection_params: dict = None):

        try:
            d = connection_params.copy()
        except AttributeError:
            if json_path is None:
                json_path = join(os.environ['GSK_HOME'], 'connection.json')
            with open(json_path, 'r') as f:
                d = json.load(f)
        finally:
            self.schema = d.pop('schema', None)

        self.connection_params = {k: d[k] for k in d.keys() & self.required}

    def query(self, query: str) -> pd.DataFrame:
        with psycopg2.connect(**self.connection_params) as conn:
            df = pd.read_sql(query, conn)
        return df

    def load_pg(self, table_name):
        """Load a postgres table into a spark dataframe."""

        with psycopg2.connect(**self.connection_params) as connection:
            df = pd.read_sql(f"select * from {table_name}", connection)
        return df

    def write_pg(self,
                 table_name: str,
                 df: pd.DataFrame,
                 on_conflict='DO NOTHING',
                 schema=None):
        """Insert values into Postgres subject to named constraint."""

        records = df.to_dict(orient="record")

        if schema is None:
            # TODO it's complicated ... hopefully we can change this later
            raise ValueError("Schema must be provided.")

        def format_if_string(x):
            return f"$${x}$$" if stringable(x) else x

        def row_vals(row):
            return ", ".join(f"{format_if_string(row[col])}" for col in df.columns)

        all_records = ", ".join(f"({row_vals(row)})" for row in records)
        query = f"""
            INSERT INTO {schema}.{table_name} ({', '.join(df.columns)}) 
            VALUES {all_records} ON CONFLICT {on_conflict}
        """

        self.sql_execute(query)

    def truncate_table(self, table_name: str, schema: str):
        """ Truncate the existing table"""

        query_string = f"""
            TRUNCATE TABLE  {schema}.{table_name}
        """
        self.sql_execute(query_string)

    def sql_execute(self, query):
        with psycopg2.connect(**self.connection_params) as conn:
            with conn.cursor() as cur:
                cur.execute(query)
            conn.commit()

    def load_market_category(self, market=None, category=None,
                             sub_category=None, only_active=False):
        """
        Load the sales data for a market/category combination.

        Parameters
        ----------
        market : str
            `market_name` to look for in `dim_market`
        category : str
            `category_name` to look for in `dim_category`
        sub_category : str
            `sub_category_name` to look for in `dim_sub_category`
        only_active : bool
            Whether or not to keep only products where `product_status_flag` is
            true. If set to `False`, all deactivated products will be returned.

        Returns
        -------
        market_category: spark DataFrame
        """

        with psycopg2.connect(**self.connection_params) as conn:
            df = pd.read_sql(
                    self.query_string(market, category, sub_category, only_active),
                    conn
            )
        return df

    # noinspection SqlResolve
    def query_string(self, market, category, sub_category, only_active=True):
        return f"""
            with this_geo as (
                select  dg.geography_id,
                        market_name,
                        channel_name,
                        retailer_name,
                        format_name,
                        segment_name
                from {self.schema}.dim_geography dg
                where market_name = '{market}' and retailer_status_flag
            ),this_category as (
                select dp.*
                from {self.schema}.dim_product dp
                join {self.schema}.hier_product hp on dp.product_id = hp.product_id
                where category_name = '{category}'
                and sub_category_name = '{sub_category}'
                {'and product_status_flag' * only_active}
            )
            select this_category.*,
                   this_geo.geography_id,
                   this_geo.channel_name,
                   this_geo.retailer_name,
                   this_geo.format_name,
                   this_geo.segment_name,
                   time_period_start,
                   time_period_end,
                   nrf_calendar_date,
                   period,
                   sales_revenue,
                   sales_units,
                   sales_revenue_incremental,
                   sales_units_incremental,
                   acv_weighted_distribution,
                   price_per_unit,
                   price_per_unit_promo,
                   price_per_unit_non_promo,
                   price_effective_price,
                   cost_amount
            from {self.schema}.fact_sales fs
            inner join this_category on this_category.product_id = fs.product_id
            inner join this_geo on this_geo.geography_id = fs.geography_id
            inner join {self.schema}.dim_time dt on fs.time_id = dt.time_id
            where this_geo.market_name = this_category.market_name
            """

    def load_market_category_all(self):

        with psycopg2.connect(**self.connection_params) as conn:
            df = pd.read_sql(self.query_string_all(), conn)
        return df

    def query_string_all(self):
        return f"""
            with this_geo as (
                select  dg.geography_id,
                        market_name,
                        channel_name,
                        retailer_name,
                        format_name,
                        segment_name
                from {self.schema}.dim_geography dg
                join {self.schema}.hier_geography hg on dg.geography_id = hg.geography_id
                where retailer_status_flag
            ),this_category as (
                select dp.*
                from {self.schema}.dim_product dp
                join {self.schema}.hier_product hp on dp.product_id = hp.product_id
            )
            select this_category.*,
                   this_geo.geography_id,
                   this_geo.channel_name,
                   this_geo.retailer_name,
                   this_geo.format_name,
                   this_geo.segment_name,
                   time_period_start,
                   time_period_end,
                   sales_revenue,
                   sales_units,
                   nrf_calendar_date,
                   sales_revenue_incremental,
                   sales_units_incremental,
                   acv_weighted_distribution,
                   price_per_unit,
                   price_per_unit_promo,
                   price_per_unit_non_promo,
                   price_effective_price,
                   cost_amount,
                   dt.period
            from {self.schema}.fact_sales fs
            inner join this_category on this_category.product_id = fs.product_id
            inner join this_geo on this_geo.geography_id = fs.geography_id
            inner join {self.schema}.dim_time dt on fs.time_id = dt.time_id
            where this_geo.market_name = this_category.market_name
            and vendor_name in ('GLAXOSMITHKLINE','GSK','GLAXOSMITHKLINE CONSUMER HEALTHCARE','GLAXOSMITHKL.C.H.','GSK (GREAT BRITAIN)')
            """
