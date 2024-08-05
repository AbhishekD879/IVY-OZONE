package com.ladbrokescoral.oxygen.cms.api.repository;

import com.ladbrokescoral.oxygen.cms.api.entity.AbstractEntity;
import com.ladbrokescoral.oxygen.cms.api.entity.timeline.TimelineChangelog;
import com.mongodb.client.FindIterable;
import org.bson.Document;

public interface TimelineChangelogRepository {

  FindIterable<Document> stream();

  <T extends AbstractEntity> void save(TimelineChangelog<T> timelineChangelog);

  <T extends AbstractEntity> TimelineChangelog<T> convert(Document object);
}
