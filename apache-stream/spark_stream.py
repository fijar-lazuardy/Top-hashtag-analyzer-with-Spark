from pyspark import SparkConf,SparkContext
from pyspark.streaming import StreamingContext
from pyspark.sql import Row,SQLContext, SparkSession
import sys
import requests

def aggregate_tags_count(new_values, total_sum):
    return sum(new_values) + (total_sum or 0)

def get_spark_session_instance(sparkConf):
    if ("sparkSessionSingletonInstance" not in globals()):
        globals()["sparkSessionSingletonInstance"] = SparkSession \
            .builder \
            .config(conf=sparkConf) \
            .getOrCreate()
    return globals()["sparkSessionSingletonInstance"]

def get_sql_context_instance(spark_context):
    if ('sqlContextSingletonInstance' not in globals()):
        globals()['sqlContextSingletonInstance'] = SQLContext(spark_context)
    return globals()['sqlContextSingletonInstance']

def process_rdd(time, rdd):
    print("----------- %s -----------" % str(time))
    try:
        # Get spark sql singleton context from the current context
        sql_context = get_sql_context_instance(rdd.context)
        # convert the RDD to Row RDD
        row_rdd = rdd.map(lambda w: Row(hashtag=w[0], hashtag_count=w[1]))
        # create a DF from the Row RDD
        hashtags_df = sql_context.createDataFrame(row_rdd)
        # Register the dataframe as table
        hashtags_df.registerTempTable("hashtags")
        # get the top 10 hashtags from the table using SQL and print them
        hashtag_counts_df = sql_context.sql("select hashtag, hashtag_count from hashtags order by hashtag_count desc limit 10")
        hashtag_counts_df.show()
        # call this method to prepare top 10 hashtags DF and send them
        send_df_to_database(hashtag_counts_df)
    except Exception as e:
#         e = sys.exc_info()[0]
#         print("Error: %s" % e)
        print(e)
        
def send_df_to_database(df):
    # extract the hashtags from dataframe and convert them into array
    top_tags = [str(t.hashtag).lower() for t in df.select("hashtag").collect()]
    # extract the counts from dataframe and convert them into array
    tags_count = [p.hashtag_count for p in df.select("hashtag_count").collect()]
    to_send = {}
    if len(top_tags) == len(tags_count):
        for i in range(len(top_tags)):
            to_send[top_tags[i]] = tags_count[i]
    print(to_send)
    # initialize and send the data through REST API
    url = 'http://34.70.144.224:5000/update-data'
    request_data = {'label': str(top_tags), 'data': str(tags_count)}
    response = requests.post(url, json=to_send)

conf = SparkConf()
conf.setAppName("TwitterStreamingApp")
# create spark instance with the above configuration
sc = SparkContext(conf=conf)
sc.setLogLevel("ERROR")
ssc = StreamingContext(sc, 5)
# setting a checkpoint to allow RDD recovery
ssc.checkpoint("checkpoint_TwitterApp")
# read data from port 9009
dstream = ssc.socketTextStream("172.30.0.6", 5678)


# split each tweet into words
words = dstream.flatMap(lambda line: line.split(" "))
hashtags = words.filter(lambda w: '#' in w).map(lambda x: (x, 1))



hashtags.foreachRDD(lambda rdd: print(rdd.collect()))
tags_totals = hashtags.updateStateByKey(aggregate_tags_count)

# do processing for each RDD generated in each interval
# tags_totals.foreachRDD(process_rdd)
tags_totals.foreachRDD(process_rdd)


ssc.start()            
ssc.awaitTermination()  