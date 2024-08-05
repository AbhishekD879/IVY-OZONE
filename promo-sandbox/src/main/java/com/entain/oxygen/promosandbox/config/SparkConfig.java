package com.entain.oxygen.promosandbox.config;

import org.apache.spark.SparkConf;
import org.apache.spark.sql.SparkSession;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.PropertySource;
import org.springframework.context.support.PropertySourcesPlaceholderConfigurer;

@Configuration
@PropertySource("classpath:application.yml")
public class SparkConfig {
  @Value("${app.name:promosandbox}")
  private String appName;

  @Value("${master.uri:local}")
  private String masterUri;

  @Value("${spark.driver.port:51810}")
  private String sparkDriverPort;

  @Value("${spark.driver.host:localhost}")
  private String sparkDriverHost;

  @Value("${spark.driver.bindAddress:localhost}")
  private String sparkDriverBindAddress;

  @Value("${spark.blockManager.port:51811}")
  private String sparkBlockManagerPort;

  @Value("${spark.cores.max}")
  private String sparkCoresMax;

  @Value("${spark.executor.memory}")
  private String sparkExecutorMemory;

  @Bean
  public SparkSession getSparkSession() {
    return SparkSession.builder().config(getSparkConf()).getOrCreate();
  }

  @Bean
  public SparkConf getSparkConf() {
    SparkConf sparkConf =
        new SparkConf()
            .setMaster(masterUri)
            .setAppName(appName)
            .set("spark.app.id", appName)
            .set("spark.driver.port", sparkDriverPort)
            .set("spark.driver.bindAddress", sparkDriverBindAddress)
            .set("spark.blockManager.port", sparkBlockManagerPort)
            .set("spark.driver.host", sparkDriverHost)
            .set("spark.shuffle.mapStatus.compression.codec", "lz4");
    if (!"0".equals(sparkCoresMax)) {
      sparkConf.set("spark.cores.max", sparkCoresMax);
    }
    if (!"0".equals(sparkExecutorMemory)) {
      sparkConf.set("spark.executor.memory", sparkExecutorMemory);
    }
    return sparkConf;
  }

  @Bean
  public static PropertySourcesPlaceholderConfigurer propertySourcesPlaceholderConfigurer() {
    return new PropertySourcesPlaceholderConfigurer();
  }
}
