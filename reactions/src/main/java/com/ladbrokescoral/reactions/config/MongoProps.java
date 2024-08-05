package com.ladbrokescoral.reactions.config;

import lombok.Data;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.stereotype.Component;

/**
 * @author PBalarangakumar 12-09-2023
 */
@Component
@ConfigurationProperties(prefix = "reactions.mongodb")
@Data
public class MongoProps {

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
