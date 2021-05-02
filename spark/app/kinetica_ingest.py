import sys
import yaml
from pyspark.sql import SparkSession
import time


def kinetica_ingest():
    start_time = time.time()
    sparkBuilder = SparkSession.builder.appName("Python Spark Kinetica Ingest")

    for k, v in sparkOpts.items():
        sparkBuilder.config(k, v)

    spark = sparkBuilder.getOrCreate();

    for k, v in hadoopOpts.items():
        spark._jsc.hadoopConfiguration().set(k, v)

    df = spark.read.format("csv").option("header", "true").load(appOpts.get('input_dir'))

    print("================ Partitions to Process ======>>>>>>>>>>>>>>")
    print(df.rdd.getNumPartitions())
    print("===========================================================")
    all_rows = df.count()
    print("----schema----")
    print(df.printSchema())
    print("--------------")

    df.write.format("com.kinetica.spark").options(**kineticaIngest).save()

    spark.stop()

    end_time = time.time()
    print("================ Export finished ====================")
    print(str(all_rows) + " datasets exported.")
    print('Execution time in seconds: %f' % (end_time - start_time))
    print("=====================================================")


if __name__ == "__main__":

    if len(sys.argv) < 1:
        print("Usage: %s <app_config.yaml>" % sys.argv[0])
        quit()

    relationalOpts = {}
    sparkOpts = {}
    kineticaIngest = {}
    hadoopOpt = {}
    appOpts = {}

    with open(sys.argv[1]) as f:
        root = yaml.load_all(f, Loader=yaml.FullLoader)

        for rootList in root:
            relationalOpts = rootList['relationalOpts']
            sparkOpts = rootList['sparkOpts']
            kineticaIngest = rootList['kineticaIngest']
            hadoopOpts = rootList['hadoopOpts']
            appOpts = rootList['appOpts']

    kinetica_ingest()
