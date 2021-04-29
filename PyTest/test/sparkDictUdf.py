'''
'''
from pyspark.sql import SparkSession, udf
#================================================================
def getLookupUdf(in_dict):
    def lookupUdf(key1, key2):
        rval = None
        if key1 in in_dict:
            if key2 in in_dict[key1]:
                rval = in_dict[key1][key2]
        return rval        
    return lookupUdf
#================================================================

spark = SparkSession.builder.appName("SimpleApp").getOrCreate()

lookupDict = {1: {'A': '1-A', 'B': '1-B'}, 
              2: {'A': '2-A', 'B': '2-B'}, 
              3: {'A': '3-A', 'B': '3-B'}}
#dict2 = spark.sparkContext.broadcast(dict1)

lookup_udf = getLookupUdf(lookupDict)
spark.udf.register("lookupUdf",lookup_udf)

df = spark.createDataFrame([[1, 'A'],[2, 'B'],[3, 'C'],[4, 'D']]).toDF("key1", "key2")
df.show(10)
df.createOrReplaceTempView("dfview")

df2 = spark.sql("select key1, key2, lookupUdf(key1, key2)   from dfview")
df2.show(10)


spark.stop()
