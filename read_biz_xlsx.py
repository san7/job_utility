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
	
df1 = pd.read_excel('提供截至10911251015_存活商號全檔_公路總局介接.xlsx', dtype = {'AGENCYCODE':object, 'BAN_NO':object, 'OLD_BAN_NO':object, 'CAPI_BAN_NO':object, \
	'BUSS_NAME':object, 'OLD_BUSS_NAME':object, 'BUSM_BUSI_LIST':object, 'BUSM_DIRECTOR_LIST':object, \
	'ORG_CODE':object, 'ORG_CODE_NAME':object, 'REG_UNIT_CODE':object, 'REG_UNIT_NAME':object, \
	'CHINA_CODE':object, 'CURR_STATUS':object, 'CURR_STATUS_DESC':object, 'BUSS_ZIPCODE':object, 'BUSS_ADDR_COMB':object, \
	'CONTACT_TEL':object, 'RES_ID':object, 'RES_NAME':object, 'RES_ADDR':object, \
	'CHG_APP_NO':object, 'LAST_CHG_NO':object, 'SET_APP_NO':object, 'CANCEL_APP_NO':object, \
	'CANCEL_WORD_NO':object, 'SUS_APP_NO':object, 'CLOSE_APP_NO':object}, converters = {'CHG_APP_DATE':INFORMIX_DATE, 'LAST_CHG_DATE':INFORMIX_DATE, \
	'SET_APP_DATE':INFORMIX_DATE, 'CANCEL_APP_DATE':INFORMIX_DATE, 'REOPEN_DATE':INFORMIX_DATE, 'REST_BEG_DATE':INFORMIX_DATE, 'REST_END_DATE':INFORMIX_DATE, \
	'CLOSE_DATE':INFORMIX_DATE, 'CLOSE_APP_DATE':INFORMIX_DATE})
df1['update_uid'] = 'tfr_criss'
df1['update_dmv'] = '00'
df1['update_src'] = '大檔'
df1['update_dt'] = 'current'
df1['file_name'] = '大檔'
print(df1)
 
sql_data = SQL_INSERT_STATEMENT_FROM_DATAFRAME(df1, 'mdm_buss_info')
#print(sql_data)

with open('mdm_biz_info.sql', 'w', encoding = 'utf-8') as f:
    for item in sql_data:
        f.write("%s;\n" % item)
		


