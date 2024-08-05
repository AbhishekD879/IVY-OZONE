package com.ladbrokescoral.oxygen.cms.configuration;

import com.ladbrokescoral.oxygen.cms.api.entity.timeline.TimelineChangelog;
import com.mongodb.client.MongoCollection;
import org.bson.Document;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Profile;
import org.springframework.data.mongodb.core.CollectionOptions;
import org.springframework.data.mongodb.core.MongoOperations;
import org.springframework.scheduling.annotation.EnableAsync;

@Profile("!UNIT")
@EnableAsync
@Configuration
public class TimelineConfig {
  private static final int CHANGELOG_SIZE_BYTES = 1000000;
  private static final int CHANGELOG_MAX_RECORDS = 10000;

  @Bean
  public MongoCollection<Document> changelogCollection(MongoOperations mongoOperations) {
    if (!mongoOperations.collectionExists(TimelineChangelog.DOCUMENT_NAME)) {
      mongoOperations.createCollection(
          TimelineChangelog.DOCUMENT_NAME,
          CollectionOptions.empty()
              .size(CHANGELOG_SIZE_BYTES)
              .maxDocuments(CHANGELOG_MAX_RECORDS)
              .capped());
    }
    return mongoOperations.getCollection(TimelineChangelog.DOCUMENT_NAME);
  }
}
