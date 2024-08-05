package com.entain.oxygen.promosandbox.utils;

import org.apache.spark.api.java.JavaSparkContext;
import org.apache.spark.sql.SparkSession;

public class SparkTestConfig {

  public static SparkSession getSparkSession() {
    return SparkSession.builder().appName("promosandbox").master("local[*]").getOrCreate();
  }

  public JavaSparkContext javaSparkContext() {
    return JavaSparkContext.fromSparkContext(getSparkSession().sparkContext());
  }
}
