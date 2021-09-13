# commonly used packages
import pyspark
from pyspark.sql.functions import *
from pyspark.ml.feature import SQLTransformer
from pyspark.sql.window import Window
import pandas as pd 
import glob
import os
import re


# load csv files

def load_sales(retailers):
  sales_file = {}
  path = '/mnt/Americas/Conformed/NA/US/Sales/Ecom/'
  for retail in retailers:
    dbfs_root = '/dbfs{}'.format(path)
    sales_path = os.path.join(dbfs_root, retail, 'Sales')
#     if the file exist
    if len(glob.glob(os.path.join(sales_path, '*.csv')))==1:
      sales_file[retail] = spark.read.csv(os.path.join(path, retail, 'Sales', '*.csv'), header=True, inferSchema=True)
    else: 
      print('{} has no or more than one sales data updated or updated is not csv format'.format(retail))
  return sales_file   


# read multiple datasource
retailers=['A','W', 'T']
cat_file=load_cat(retailers)
sales_file = load_sales(retailers)

# Use RE to cleanup the cell values

def cleanup_col(retailer:str, file = 'sales_file'):
  col = []
  old_col = eval(file)[retailer].columns
  for i in range(len(old_col)):
    col.append(re.sub('\W', '', eval(file)[retailer].columns[i]))
  eval(file)[retailer] = eval(file)[retailer].toDF(*col)
  
# spark df display
sales_file['Target'].limit(100).display()

# spark sql

spark.sql('select * from sales_file['Target']')

# Other way to use sql in pyspark
from pyspark.ml.feature import SQLTransformer
sqlTrans = SQLTransformer(statement = 'select Product_Name,TCIN, count(Item) as count from __THIS__ group by Product_Name,TCIN ')
result1 = sqlTrans.transform(sales_file['Target'])
result1.limit(1000).display()

sqlTrans = SQLTransformer(statement = 'select ProductName,count(distinct upc) as upc_count from __THIS__ group by ProductName')
result1 = sqlTrans.transform(wsdf)

# sort the df
result1 = result1.sort('Product_Name', desc('count'), 'TCIN', )
result1.display()

# this cell is to find the first one in the group. 
# for example, if we want to only keep the most frequent TCIN for a same product name, the code will be like below
window = Window.partitionBy("Product_Name").orderBy(desc('count'))
 
result1.withColumn('rank', rank().over(window))\
 .filter(col('rank') == 1).drop('rank')\
 .display()


# spark create df and define the data type of each column
import pyspark.sql.types as st

user_schema = st.StructType([
    st.StructField(col[0], st.StringType(), True),
    st.StructField(col[1], st.StringType(), True),
    st.StructField(col[2], st.StringType(), True),
  st.StructField(col[3], st.StringType(), True),
  st.StructField(col[4], st.StringType(), True)
])

walmart_sdf = spark.createDataFrame(walmart.loc[1:,:4], schema = user_schema)

# change column data type
wsdf = walmart_sdf.withColumn('upc',walmart_sdf['Dim_WmItemNbr'].cast(IntegerType()))
wsdf.columns

# filter the df
result1.filter(result1[1]>1).display()


