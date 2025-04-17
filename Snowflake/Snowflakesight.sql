-- this is done in Snowsight , the UI

-- set the role
USE ROLE accountadmin;

-- set the virtual warehouse
use WHAREHOUSE compute_wh;

-- STEPS: CREATE DB, CREATE SCHEMA, CREATE TABLE

-- create the Taste Bytes db
CREATE OR REPLACE DATABASE tasty_bytes_sample_data;

-- create the raw POS (point-of-sale) schema
CREATE OR REPLACE SCHEMA tasty_bytes_sample_data.raw_pos;

-- create the raw Menu table
CREATE OR REPLACE TABLE tasty_bytes_sample_data.raw_pos.menu
{
    menu_id NUMBER(19.0),
    menu_type_id NUMBER(38.0),
    menu_type VARCHAR(16777216),
    truck_brand_name VARCHAR(16777216),
    menu_item_id NUMBER(38.0),
    menu_item_name VARCHAR(16777216),
    item_category VARCHAR(16777216),
    item_subcategory VARCHAR(16777216),
    cost_of_goods_usd NUMBER(38.4),
    sale_price_usd NUMBER(28.4),
    menu_item_health_metrics_obs VARIANT
}

-- confirm empty Menu table exists
select * from tasty_bytes_sample_data.raw_pos.menu;

-- STEP 3 to connect to the Blob storage, let's create a stage

-- create the Stage referencing the Blob location and CSV file format
-- stage references a publicly available S3 bucket  
-- stage is a temporary storage area for raw data files
CREATE OR REPLACE STAGE tasty_bytes_sample_data.public.blob_stage
url = 's3://sfquickstarts/tastybytes/'
file_format = (type = csv);

-- query the stage to find the Menu CSV file
LIST @tasty_bytes_sample_data.public.blob_stage/raw_pos/menu/;

-- STEP 4: Now let's load the Menu CSV file from the stage

-- copy the Menu CSV file into the Menu table
COPY INTO tasty_bytes_sample_data.raw_pos.menu
FROM @tasty_bytes_sample_data.public.blob_stage/raw_pos/menu/;

-- how many rows are in the table?
select count(*) as N from tasty_bytes_sample_data.raw_pos.menu;

-- what menu items des the Freezing Point brand sell?
select menu_item_name
from tasty_bytes_sample_data.raw_pos.menu
where truck_brand_name = 'Freezing Point';

-- extracting fields from JSON formatted file (ELT)
-- extracting Mango Sticky rice ingredients from the semi-structured col
select m.menu_item_name,
        obj.value:"ingredients"::ARRAY as ingredients
from  tasty_bytes_sample_data.raw_pos.menu m,
        LATERAL FLATTEN (input => m.menu_item_health_metrics_obj:menu_item_health_metrics) obj
where truck_brand_name = 'Freezing Point'
and menu_item_name = 'Mango Sticky Rice';