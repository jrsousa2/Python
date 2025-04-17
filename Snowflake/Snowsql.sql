-- REMINDER NOTES FOR snowsql

--type in the cmd prompt C:\ (-a account_name -u user_name)
snowsql -a bbpwphe-qn15026 -u SDATALABS
-- app will install if first time running the cmd supposedly
-- pwd prompt
-- SnowSQL * v1.2.31
--Type  SQL statement or help
SDATALABS#COMPUTE_WH@(no database).(no schema)>use SNOWFLAKE_SAMPLE_DATA;

SDATALABS#COMPUTE_WH@SNOWFLAKE_SAMPLE_DATA.(no schema)> use schema TPCDS_SF100TCL;

SDATALABS#COMPUTE_WH@SNOWFLAKE_SAMPLE_DATA.TPCDS_SF100TCL>select top 5 from SNOWFLAKE_SAMPLE_DATA.TPCDS_SF100TCL.CUSTOMER_ADDRESS;
