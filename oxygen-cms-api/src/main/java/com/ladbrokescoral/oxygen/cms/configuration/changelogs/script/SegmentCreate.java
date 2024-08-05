package com.ladbrokescoral.oxygen.cms.configuration.changelogs.script;

import com.github.cloudyrock.mongock.driver.mongodb.springdata.v3.decorator.impl.MongockTemplate;
import com.ladbrokescoral.oxygen.cms.api.entity.segment.Segment;
import com.ladbrokescoral.oxygen.cms.api.entity.segment.SegmentConstants;

public class SegmentCreate {

  public void addSegment(MongockTemplate mongockTemplate) {
    // Do nothing as we are going to create the Segments/segmentedModules specific to Brand. Not
    // deleting the Changelog as it is executed in some environments already.
    // Data clean up will taken care while adding the records with respect to brand.
  }

  public void addSegment(MongockTemplate mongockTemplate, String brand) {

    Segment segment =
        Segment.builder()
            .segmentName(SegmentConstants.UNIVERSAL)
            .isActive(true)
            .brand(brand)
            .build();
    mongockTemplate.insert(segment);
  }
}
