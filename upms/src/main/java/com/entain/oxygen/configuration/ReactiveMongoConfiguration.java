package com.entain.oxygen.configuration;

import com.entain.oxygen.util.EncryptAndDecryptUtil;
import com.mongodb.ConnectionString;
import com.mongodb.MongoClientSettings;
import com.mongodb.reactivestreams.client.MongoClient;
import com.mongodb.reactivestreams.client.MongoClients;
import java.net.URLEncoder;
import java.nio.charset.StandardCharsets;
import lombok.extern.slf4j.Slf4j;
import org.apache.commons.lang3.StringUtils;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.context.properties.EnableConfigurationProperties;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.data.mongodb.config.AbstractReactiveMongoConfiguration;
import org.springframework.data.mongodb.config.EnableReactiveMongoAuditing;
import org.springframework.data.mongodb.core.ReactiveMongoTemplate;
import org.springframework.data.mongodb.core.SimpleReactiveMongoDatabaseFactory;

@Configuration
@EnableReactiveMongoAuditing
@EnableConfigurationProperties(MongoDbProperties.class)
@Slf4j
public class ReactiveMongoConfiguration extends AbstractReactiveMongoConfiguration {

  private final MongoDbProperties mongoDbProperties;
  private final String enviroment;
  private final String defaultUri;

  public ReactiveMongoConfiguration(
      MongoDbProperties mongoDbProperties,
      @Value("${upms.profile:high}") String enviroment,
      @Value("${mongodb.uri}") String defaultUri) {
    this.mongoDbProperties = mongoDbProperties;
    this.enviroment = enviroment;
    this.defaultUri = defaultUri;
  }

  @Override
  public String getDatabaseName() {
    return mongoDbProperties.getDbName();
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
    if (this.enviroment.equalsIgnoreCase("default")) {
      return defaultUri;
    }
    EncryptAndDecryptUtil.setSecretKey(
        mongoDbProperties.getPasswordKeyfile(), mongoDbProperties.getAlgorithm());
    password =
        EncryptAndDecryptUtil.readString(
            mongoDbProperties.getPasswordFile(), mongoDbProperties.getAlgorithm());
    password = URLEncoder.encode(password, StandardCharsets.UTF_8);
    connectionString
        .append("mongodb://")
        .append(mongoDbProperties.getMongoUser())
        .append(":")
        .append(password)
        .append("@")
        .append(mongoDbProperties.getDbHosts())
        .append("/")
        .append(mongoDbProperties.getDbName());
    if (StringUtils.isNotEmpty(mongoDbProperties.getAuthSource())) {
      connectionString.append("?authSource=").append(mongoDbProperties.getAuthSource());
    }
    if (StringUtils.isNotEmpty(mongoDbProperties.getReplicaSet())) {
      connectionString.append("&replicaSet=").append(mongoDbProperties.getReplicaSet());
    }
    return connectionString.toString();
  }

  @Override
  public boolean autoIndexCreation() {
    return true;
  }

  @Bean
  public ReactiveMongoTemplate reactiveMongoTemplate() {
    return new ReactiveMongoTemplate(
        new SimpleReactiveMongoDatabaseFactory(reactiveMongoClient(), getDatabaseName()));
  }
}
