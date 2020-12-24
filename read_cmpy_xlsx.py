import pandas as pd

def SQL_INSERT_STATEMENT_FROM_DATAFRAME(SOURCE, TARGET):
    sql_texts = []
    for index, row in SOURCE.iterrows():
        tmp = 'INSERT INTO '+TARGET+' ('+ str(', '.join(SOURCE.columns))+ ') VALUES '+ str(tuple(row.values))
        tmp = tmp.replace('nan', 'null')
        #tmp = tmp.replace('Timestamp', '')
        tmp = tmp.replace('NaT', 'null')
        tmp = tmp.replace('\'current\'', 'current')
        sql_texts.append(tmp)        
    return sql_texts

# from YYYYMMDD to MM/DD/YYYY
def INFORMIX_DATE(source):
    if(len(source) == 8):
        year = source[0:4]
        month = source[4:6]
        day = source[6:8]
        return month + "/" + day + "/" + year
    return source
	
#df1 = pd.read_excel('data.xlsx', parse_dates = ['CHG_APP_DATE','ESTAB_APP_DATE','LQDN_APP_DATE','REVOKE_APP_DATE','SUS_BEG_DATE','SUS_END_DATE','SUS_APP_DATE'], \
#	dtype = {'BAN_NO CHAR':object, 'OLD_BAN_NO':object, 'CMPY_NAME LVARCHAR':object, 'ORG_TYPE':object, \
#		'ORG_TYPE_NAME':object, 'REG_UNIT_CODE':object, 'REG_UNIT_NAME':object, 'CHINA_CODE':object, \
#		'CMPY_STATUS':object, 'CMPY_STATUS_DESC':object, 'CMPY_ZIP_CODE':object, 'CMPY_ADD':object, \
#		'CMPY_TEL_NO':object, 'RES_ID':object, 'REP_NAME':object, 'CHG_APP_WD':object, 'CHG_APP_NO':object, \
#		'ESTAB_APP_WD':object, 'ESTAB_APP_NO':object, 'LQDN_APP_WD':object, 'LQDN_APP_NO':object, \
#		'REVOKE_APP_WD':object, 'REVOKE_APP_NO':object, 'CASE_STATUS':object, 'CASE_STATUS_DESC':object, \
#		'SUS_APP_WD':object, 'SUS_APP_NO':object})

df1 = pd.read_excel('提供截至10911251015_存活公司全檔_公路總局介接_2.xlsx', dtype = {'BAN_NO':object, 'OLD_BAN_NO':object, 'CMPY_NAME':object, 'ORG_TYPE':object, \
	'ORG_TYPE_NAME':object, 'REG_UNIT_CODE':object, 'REG_UNIT_NAME':object, 'CHINA_CODE':object, \
	'CMPY_STATUS':object, 'CMPY_STATUS_DESC':object, 'CMPY_ZIP_CODE':object, 'CMPY_ADD':object, \
	'CMPY_TEL_NO':object, 'RES_ID':object, 'REP_NAME':object, 'CHG_APP_WD':object, 'CHG_APP_NO':object, \
	'ESTAB_APP_WD':object, 'ESTAB_APP_NO':object, 'LQDN_APP_WD':object, 'LQDN_APP_NO':object, \
	'REVOKE_APP_WD':object, 'REVOKE_APP_NO':object, 'CASE_STATUS':object, 'CASE_STATUS_DESC':object, \
	'SUS_APP_WD':object, 'SUS_APP_NO':object}, converters = {'CHG_APP_DATE':INFORMIX_DATE, 'ESTAB_APP_DATE':INFORMIX_DATE, 'LQDN_APP_DATE':INFORMIX_DATE, \
	'REVOKE_APP_DATE':INFORMIX_DATE, 'SUS_BEG_DATE':INFORMIX_DATE, 'SUS_END_DATE':INFORMIX_DATE, 'SUS_APP_DATE':INFORMIX_DATE})
df1['update_uid'] = 'tfr_criss'
df1['update_dmv'] = '00'
df1['update_src'] = '大檔'
df1['update_dt'] = 'current'
df1['file_name'] = '大檔'
print(df1)
 
sql_data = SQL_INSERT_STATEMENT_FROM_DATAFRAME(df1, 'mdm_cmpy_info')
#print(sql_data)

with open('mdm_cmpy_info_2.sql', 'w', encoding = 'utf-8') as f:
    for item in sql_data:
        f.write("%s;\n" % item)
		


