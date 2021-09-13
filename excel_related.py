# Read excel
cost_map = pd.read_excel(
                f"{path}/{market}/{category}_MARGIN.xlsx", sheet_name="MarginCost")


# Write df to excel sheets
# call the class 
writer = pd.ExcelWriter(excel_sheet_path, engine='xlsxwriter')
# name the sheet
sheets_to_create = dict(newly_added=new_prod, lapsed_prod=lapsed_prod, cs_changed_prod=cs_changed_prod,
                        sales_change=output_sales)
# create a loop to add multiple sheets in the excel output
for name, data in sheets_to_create.items():
    data.to_excel(writer, sheet_name=name, index=False)
    worksheet = writer.sheets[name]
    col_names = [{'header': col_name} for col_name in data.columns]
    worksheet.add_table(0, 0, data.shape[0], data.shape[1] - 1,
                        {'columns': col_names,
                         'style': 'Table Style Medium 21',
                         'name': name})
    worksheet.set_column('A:Z', 36)
# print status
print(f'Writing output to {excel_sheet_path}')
# save
writer.save()
