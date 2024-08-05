package com.entain.oxygen.promosandbox.config;

import com.entain.oxygen.promosandbox.utils.EncryptAndDecryptUtil;
import com.mongodb.ConnectionString;
import java.util.List;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.autoconfigure.mongo.MongoClientSettingsBuilderCustomizer;
import org.springframework.boot.context.properties.EnableConfigurationProperties;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
@EnableConfigurationProperties(MongoDbProperties.class)
public class MongoDbConfiguration {

  @Bean
  public MongoClientSettingsBuilderCustomizer mongoClient(
      @Value("${spring.data.mongodb.uri}") String mongoUri,
      @Value("${promosandbox.distributed.prefix:LOCAL}") String activeProfile,
      @Value("${promosandbox.environments}") List<String> environments,
      MongoDbProperties mongoDbProperties) {
    String mongoDbUri = constructMongoUri(mongoUri, activeProfile, mongoDbProperties, environments);
    ConnectionString connection = new ConnectionString(mongoDbUri);
    return settings -> settings.applyConnectionString(connection);
  }

  private String constructMongoUri(
      String mongoDbUri,
      String activeProfile,
      MongoDbProperties mongoDbProperties,
      List<String> environments) {
    final StringBuilder mongoUri = new StringBuilder();
    final String password;
    if (environments.contains(activeProfile)) {
      EncryptAndDecryptUtil.setSecretKey(
          mongoDbProperties.getPasswordKeyfile(), mongoDbProperties.getAlgorithm());
      password =
          EncryptAndDecryptUtil.readString(
              mongoDbProperties.getPasswordFile(), mongoDbProperties.getAlgorithm());
      mongoUri.append("mongodb://");
      mongoUri.append(mongoDbProperties.getMongoUser());
      mongoUri.append(":");
      mongoUri.append(password);
      mongoUri.append("@");
      mongoUri.append(mongoDbProperties.getDbHosts());
      mongoUri.append("/");
      mongoUri.append(mongoDbProperties.getDbName());
      mongoUri.append("?authSource=");
      mongoUri.append(mongoDbProperties.getAuthSource());
      mongoUri.append("&replicaSet=");
      mongoUri.append(mongoDbProperties.getReplicaSet());
    } else {
      mongoUri.append(mongoDbUri);
    }
    return mongoUri.toString();
  }
}
