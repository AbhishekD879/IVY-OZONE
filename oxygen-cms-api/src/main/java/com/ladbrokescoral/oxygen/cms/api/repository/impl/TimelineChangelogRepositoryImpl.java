package com.ladbrokescoral.oxygen.cms.api.repository.impl;

import com.ladbrokescoral.oxygen.cms.api.entity.AbstractEntity;
import com.ladbrokescoral.oxygen.cms.api.entity.timeline.TimelineChangelog;
import com.ladbrokescoral.oxygen.cms.api.repository.TimelineChangelogRepository;
import com.mongodb.CursorType;
import com.mongodb.client.FindIterable;
import com.mongodb.client.MongoCollection;
import java.time.Instant;
import lombok.RequiredArgsConstructor;
import org.bson.Document;
import org.springframework.data.mongodb.core.MongoTemplate;
import org.springframework.stereotype.Repository;

@Repository
@RequiredArgsConstructor
public class TimelineChangelogRepositoryImpl implements TimelineChangelogRepository {

  // FIXME: not common usage as others, any reason ?
  private final MongoTemplate mongoTemplate;
  private final MongoCollection<Document> changelogCollection;

  @Override
  public <T extends AbstractEntity> void save(TimelineChangelog<T> timelineChangelog) {
    mongoTemplate.save(timelineChangelog, TimelineChangelog.DOCUMENT_NAME);
  }

  @Override
  public FindIterable<Document> stream() {
    Instant now = Instant.now();
    return changelogCollection
        .find()
        .cursorType(CursorType.TailableAwait)
        .filter(new Document("timestamp", new Document("$gte", now)));
  }

  @Override
  public <T extends AbstractEntity> TimelineChangelog<T> convert(Document object) {
    return mongoTemplate.getConverter().read(TimelineChangelog.class, object);
  }
}
