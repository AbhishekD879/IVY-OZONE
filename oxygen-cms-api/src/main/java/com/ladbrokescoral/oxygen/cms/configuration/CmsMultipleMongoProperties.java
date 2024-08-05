package com.ladbrokescoral.oxygen.cms.configuration;

import lombok.Data;
import org.springframework.boot.autoconfigure.mongo.MongoProperties;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.context.annotation.Profile;

@Data
@ConfigurationProperties(prefix = "mongodb")
@Profile("!UNIT")
public class CmsMultipleMongoProperties {

  private MongoProperties cmsApi = new MongoProperties();
  private MongoProperties cmsArchival = new MongoProperties();
  private MongoProperties cmsArchivalJobs = new MongoProperties();
}
