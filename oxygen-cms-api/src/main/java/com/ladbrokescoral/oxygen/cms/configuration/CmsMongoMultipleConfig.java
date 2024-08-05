package com.ladbrokescoral.oxygen.cms.configuration;

import com.mongodb.ConnectionString;
import com.mongodb.MongoClientSettings;
import com.mongodb.client.MongoClient;
import com.mongodb.client.MongoClients;
import lombok.RequiredArgsConstructor;
import org.springframework.boot.autoconfigure.mongo.MongoProperties;
import org.springframework.boot.context.properties.EnableConfigurationProperties;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Profile;
import org.springframework.data.mongodb.core.MongoTemplate;

@Configuration
@RequiredArgsConstructor
@EnableConfigurationProperties(CmsMultipleMongoProperties.class)
@Profile("!UNIT")
public class CmsMongoMultipleConfig {

  private final CmsMultipleMongoProperties mongoProperties;

  @Bean(name = "cmsArchivalMongoTemplate")
  public MongoTemplate cmsArchivalMongoTemplate() {
    return new MongoTemplate(
        getCmsArchivalmongoClient(this.mongoProperties.getCmsArchival()),
        this.mongoProperties.getCmsArchival().getDatabase());
  }

  @Bean(name = "cmsArchivalMongoJobTemplate")
  public MongoTemplate cmsArchivalMongoJobTemplate() {
    return new MongoTemplate(
        getCmsArchivalJobsmongoClient(this.mongoProperties.getCmsArchivalJobs()),
        this.mongoProperties.getCmsArchivalJobs().getDatabase());
  }

  @Bean
  public MongoClient getCmsArchivalmongoClient(MongoProperties cmsArchivalmongoProperties) {
    final ConnectionString connectionString =
        new ConnectionString(cmsArchivalmongoProperties.getUri());
    final MongoClientSettings mongoClientSettings =
        MongoClientSettings.builder().applyConnectionString(connectionString).build();
    return MongoClients.create(mongoClientSettings);
  }

  @Bean
  public MongoClient getCmsArchivalJobsmongoClient(MongoProperties cmsArchivalJobsmongoProperties) {
    final ConnectionString connectionString =
        new ConnectionString(cmsArchivalJobsmongoProperties.getUri());
    final MongoClientSettings mongoClientSettings =
        MongoClientSettings.builder().applyConnectionString(connectionString).build();
    return MongoClients.create(mongoClientSettings);
  }
}
