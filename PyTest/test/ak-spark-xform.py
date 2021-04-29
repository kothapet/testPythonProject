#######################################################################################################################################
# ETL Transform : Initial version
#
#
#
#
#######################################################################################################################################

import logging
import sys
import boto3
import time
import csv
import json

from datetime import datetime, timedelta, date
from pyspark.sql import SparkSession
#from pyspark.sql.functions import *
from pyspark.sql import functions as F
from pyspark.sql.types import *
 
#===================================================================================================
def getJsonLocalData(i_fileFullPath):
    
    try:
        f = open(i_fileFullPath)
        data = json.load(f)
    except Exception as e:
        raise e
    
    print(json.dumps(data, indent=2, sort_keys=False))
    return data

def getJsonS3Data(i_s3Bucket, i_s3Key):
    
    try:
        s3 = boto3.client('s3')
        data = s3.get_object(Bucket=i_s3Bucket, Key=i_s3Key)
        json_data = data['Body'].read().decode('utf-8')
        data = json.loads(json_data)
    except Exception as e:
        raise e
    
    print(json.dumps(data, indent=2, sort_keys=False))
    return data

def processInputs(i_spark, i_inputMetaData):
    
    dfDict = {}
    try:
        for item1 in i_inputMetaData:
            print(item1)
            path = "s3a://"
            if "Location" in item1:
                location = item1["Location"]
                if location == 'hdfs':
                    path = "hdfs:///"
                elif location == 'file':
                    path = "file:///"

            fileName = path + item1["formatted_path"] + "/" + item1["formatted_key"]
            print('fileName : ', fileName)
            tempDf = i_spark.read.parquet(fileName)
                
            viewName = item1["ViewName"]
            dfDict[viewName] = tempDf
            
            if "PartitionKeys" in item1 and "NumPartitions" in item1:
                dfDict[viewName] = dfDict[viewName].repartition(int(item1["NumPartitions"]), *item1["PartitionKeys"])
            elif "NumPartitions" in item1:
                dfDict[viewName] = dfDict[viewName].repartition(int(item1["NumPartitions"]))
            elif "PartitionKeys" in item1:
                dfDict[viewName] = dfDict[viewName].repartition(*item1["PartitionKeys"])
                
            if "Cache" in item1:
                if item1["Cache"]:
                    dfDict[viewName].cache()
                    
            dfDict[viewName].createOrReplaceTempView(viewName)
            
    except Exception as e:
        raise e
    
    return dfDict

def processTransformations(i_spark, i_dataframes, i_transformMetaData):
    
    dfDict = i_dataframes
    try:
        for idx1 in i_transformMetaData:
            print(idx1)
            item1 = i_transformMetaData[idx1]
            
            viewName = item1["ViewName"]
            if "SparkQuery" in item1:
                dfDict[viewName] = i_spark.sql(item1["SparkQuery"])
            elif "SparkTransform" in item1:
                exec(item1["SparkTransform"])
            else:
                raise ValueError('SparkQuery or SparkTransform are missing. One of the option is needed.')    
                
            if "PartitionKeys" in item1 and "NumPartitions" in item1:
                dfDict[viewName] = dfDict[viewName].repartition(int(item1["NumPartitions"]), *item1["PartitionKeys"])
            elif "NumPartitions" in item1:
                dfDict[viewName] = dfDict[viewName].repartition(int(item1["NumPartitions"]))
            elif "PartitionKeys" in item1:
                dfDict[viewName] = dfDict[viewName].repartition(*item1["PartitionKeys"])
                
            if "Cache" in item1:
                if item1["Cache"]:
                    dfDict[viewName].cache()
                    
            dfDict[viewName].createOrReplaceTempView(viewName)
                    
            
    except Exception as e:
        raise e
    
    return dfDict

def processOutputs(i_spark, i_dataframes, i_outputMetaData):
    
    try:
        for item1 in i_outputMetaData:
            print(item1)
                
            viewName = item1["ViewName"]
            tempDf = i_dataframes[viewName]
            
            fileFormat = "csv"
            if "TargetFormat" in item1:
                fileFormat = item1["TargetFormat"]
            
            writeMode = "error"
            if "SparkSaveMode" in item1:
                writeMode = item1["SparkSaveMode"]
            
            path = "s3a://"
            if "Location" in item1:
                location = item1["Location"]
                if location == 'hdfs':
                    path = "hdfs:///"
                elif location == 'file':
                    path = "file:///"

            fileName = path + item1["formatted_path"] + "/" + item1["formatted_key"]
            print('fileName : ', fileName)
            tempDf.write.format(fileFormat).mode(writeMode).save(fileName)
            
    except Exception as e:
        raise e

#===================================================================================================
LOGGER = logging.getLogger("com.aws.gwf")
LOGGER.setLevel(logging.INFO)

LOGGER.info('Starting ak-spark-etl-transform : ', datetime.now().strftime('%m/%d/%Y %H:%M:%S'))
#---------------------------------------------------------------------------------------------------
process_status="Successful"

meta_bucket =  'dev-gwf-cc-raw-class0-us-east-1'
meta_key = 'metadata/ETL_SPARK.json'
try:
    #meta_data = getJsonS3Data(meta_bucket, meta_key)
    meta_data = getJsonLocalData('D:/Users/nndkth/eclipse-workspace/PySparkTest/ETL_SPARK.json')

    spark = SparkSession.builder \
                        .appName("Spark ETL") \
                        .getOrCreate()

    #spark.sparkContext.setLogLevel('WARN')                       
    '''
    # to get default credentials                     
    # to specify credentials                     
    spark._jsc.hadoopConfiguration().set("fs.s3a.awsAccessKeyId", "[ACCESS KEY]")
    spark._jsc.hadoopConfiguration().set("fs.s3a.awsSecretAccessKey", "[SECRET KEY]")
    # SSE-KMS doesn't work in 2.8.5
    spark._jsc.hadoopConfiguration().set("fs.s3a.server-side-encryption-algorithm", "SSE-KMS")
    spark._jsc.hadoopConfiguration().set("fs.s3a.server-side-encryption.key", "arn:aws:kms:us-east-1:716303183772:key/f76ea1ee-a179-4992-96df-c6764cfca460")
    '''
    spark._jsc.hadoopConfiguration().set("f3.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
    spark._jsc.hadoopConfiguration().set("f3.s3a.region", "us-east-1")
    spark._jsc.hadoopConfiguration().set("mapreduce.fileoutputcommitter.algorithm.version", "2")
    spark._jsc.hadoopConfiguration().set("fs.s3a.aws.credentials.provider", "com.amazonaws.auth.DefaultAWSCredentialsProviderChain")
    
    dataframes = {}
    
    if "inputs" in meta_data:
        dataframes = processInputs(spark, meta_data["inputs"])
    else:
        raise Exception("Atleast one input is required exception")
    
    for key1 in dataframes:
        dataframes[key1].printSchema()
        dataframes[key1].show(10)
        
    if "transformations" in meta_data:
        dataframes = processTransformations(spark, dataframes, meta_data["transformations"])
    
    for key1 in dataframes:
        dataframes[key1].printSchema()
        dataframes[key1].show(10)
    
    if "outputs" in meta_data:
        processOutputs(spark, dataframes, meta_data["outputs"])
    else:
        raise Exception("Atleast one input is required exception")
        
except Exception as e:
    LOGGER.fatal("Encountered and Error: " +  str(error))
    process_status="Failure"
    raise e
finally:
    LOGGER.info(process_status, ' ak-spark-etl-transform : ', datetime.now().strftime('%m/%d/%Y %H:%M:%S'))
#---------------------------------------------------------------------------------------------------


