package com.ladbrokescoral.oxygen.cms.api.entity.segment;

import com.ladbrokescoral.oxygen.cms.api.entity.AbstractSportEntity;
import com.ladbrokescoral.oxygen.cms.api.service.validators.SegmentNamePattern;
import java.util.ArrayList;
import java.util.List;
import lombok.Data;
import lombok.EqualsAndHashCode;
import org.springframework.data.mongodb.core.mapping.Field;

@Data
@EqualsAndHashCode(callSuper = true)
public abstract class AbstractSportSegmentEntity extends AbstractSportEntity
    implements SegmentEntity {

  private List<SegmentReference> segmentReferences = new ArrayList<>();
  private List<@SegmentNamePattern String> exclusionList = new ArrayList<>();
  private List<@SegmentNamePattern String> inclusionList = new ArrayList<>();
  private List<String> fanzoneInclusions = new ArrayList<>();
  private String archivalId;

  @Field(value = "applyUniversalSegments")
  private boolean universalSegment = Boolean.TRUE;

  private String message;
}
