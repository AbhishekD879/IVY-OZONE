package com.entain.oxygen.configuration;

import lombok.Data;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.stereotype.Component;

@Component
@ConfigurationProperties(prefix = "upms.mongodb")
@Data
public class MongoDbProperties {

  private String mongoUser;

  private String dbHosts;

  private String dbName;

  private String authSource;

  private String replicaSet;

  private String passwordFile;

  private String passwordKeyfile;

  private String algorithm;

  private Index index;

  @Data
  static class Index {
    private String collectionNames;
    private String indexNames;
  }
}
