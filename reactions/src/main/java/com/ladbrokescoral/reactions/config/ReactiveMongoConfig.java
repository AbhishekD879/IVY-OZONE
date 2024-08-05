package com.ladbrokescoral.reactions.config;

import com.ladbrokescoral.reactions.util.EncryptAndDecryptUtil;
import com.mongodb.ConnectionString;
import com.mongodb.MongoClientSettings;
import com.mongodb.reactivestreams.client.MongoClient;
import com.mongodb.reactivestreams.client.MongoClients;
import java.net.URLEncoder;
import java.nio.charset.StandardCharsets;
import org.apache.commons.lang3.StringUtils;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.context.properties.EnableConfigurationProperties;
import org.springframework.context.annotation.Configuration;
import org.springframework.data.mongodb.config.AbstractReactiveMongoConfiguration;

/**
 * @author PBalarangakumar 12-09-2023
 */
@Configuration
@EnableConfigurationProperties(MongoProps.class)
public class ReactiveMongoConfig extends AbstractReactiveMongoConfiguration {

  private final String enviroment;
  private final MongoProps mongoProps;

  public ReactiveMongoConfig(
      @Value("${spring.profiles.active}") String enviroment, MongoProps mongoProps) {
    this.enviroment = enviroment;
    this.mongoProps = mongoProps;
  }

  @Override
  public String getDatabaseName() {
    return mongoProps.getDbName();
  }

  @Override
  public MongoClient reactiveMongoClient() {
    String uri = formConnectionString();
    ConnectionString connectionString = new ConnectionString(uri);
    MongoClientSettings mongoClientSettings =
        MongoClientSettings.builder().applyConnectionString(connectionString).build();
    return MongoClients.create(mongoClientSettings);
  }

  private String formConnectionString() {
    StringBuilder connectionString = new StringBuilder();

    String password;
    if (this.enviroment.equalsIgnoreCase("LOCAL")) {
      return connectionString.append("mongodb://").append(mongoProps.getDbHosts()).toString();
    }
    EncryptAndDecryptUtil.setSecretKey(mongoProps.getPasswordKeyfile(), mongoProps.getAlgorithm());
    password =
        EncryptAndDecryptUtil.readString(mongoProps.getPasswordFile(), mongoProps.getAlgorithm());
    password = URLEncoder.encode(password, StandardCharsets.UTF_8);
    connectionString
        .append("mongodb://")
        .append(mongoProps.getMongoUser())
        .append(":")
        .append(password)
        .append("@")
        .append(mongoProps.getDbHosts())
        .append("/")
        .append(mongoProps.getDbName());
    if (StringUtils.isNotEmpty(mongoProps.getAuthSource())) {
      connectionString.append("?authSource=").append(mongoProps.getAuthSource());
    }
    if (StringUtils.isNotEmpty(mongoProps.getReplicaSet())) {
      connectionString.append("&replicaSet=").append(mongoProps.getReplicaSet());
    }
    return connectionString.toString();
  }

  @Override
  public boolean autoIndexCreation() {
    return true;
  }
}
