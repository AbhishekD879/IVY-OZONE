package com.ladbrokescoral.oxygen.cms.configuration;

import com.github.cloudyrock.spring.v5.EnableMongock;
import com.mongodb.ConnectionString;
import com.mongodb.MongoClientSettings;
import com.mongodb.client.MongoClient;
import com.mongodb.client.MongoClients;
import lombok.RequiredArgsConstructor;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Primary;
import org.springframework.context.annotation.Profile;
import org.springframework.data.mongodb.config.AbstractMongoClientConfiguration;
import org.springframework.data.mongodb.config.EnableMongoAuditing;
import org.springframework.data.mongodb.core.MongoTemplate;
import org.springframework.data.mongodb.repository.config.EnableMongoRepositories;

@Configuration
@EnableMongoRepositories(basePackages = "com.ladbrokescoral.oxygen.cms.api.repository")
@EnableMongock
@EnableMongoAuditing
@Profile("!UNIT")
@RequiredArgsConstructor
public class CmsApiMongoConfig extends AbstractMongoClientConfiguration {

  private final CmsMultipleMongoProperties mongoProperties;

  @Override
  protected String getDatabaseName() {
    return mongoProperties.getCmsApi().getDatabase();
  }

  @Override
  protected boolean autoIndexCreation() {
    return true;
  }

  @Primary
  @Bean
  public MongoTemplate cmsApiMongoTemplate() {
    return new MongoTemplate(mongoClient(), this.mongoProperties.getCmsApi().getDatabase());
  }

  @Bean
  @Primary
  @Override
  public MongoClient mongoClient() {
    ConnectionString connectionString = new ConnectionString(mongoProperties.getCmsApi().getUri());
    MongoClientSettings mongoClientSettings =
        MongoClientSettings.builder().applyConnectionString(connectionString).build();

    return MongoClients.create(mongoClientSettings);
  }
}
