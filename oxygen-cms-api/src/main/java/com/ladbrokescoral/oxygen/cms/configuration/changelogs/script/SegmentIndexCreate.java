package com.ladbrokescoral.oxygen.cms.configuration.changelogs.script;

import com.github.cloudyrock.mongock.driver.mongodb.springdata.v3.decorator.impl.MongockTemplate;
import com.ladbrokescoral.oxygen.cms.api.entity.segment.Segment;
import org.bson.Document;
import org.springframework.data.mongodb.core.index.CompoundIndexDefinition;
import org.springframework.data.mongodb.core.index.IndexDefinition;

public class SegmentIndexCreate {
  public void createIndex(MongockTemplate mongockTemplate) {
    IndexDefinition index =
        new CompoundIndexDefinition(new Document().append("brand", 1).append("segmentName", 1))
            .unique()
            .named("brand_segmentName_unique");
    mongockTemplate.indexOps(Segment.class).ensureIndex(index);
  }
}
