package com.ladbrokescoral.oxygen.cms.api.entity.segment;

import com.ladbrokescoral.oxygen.cms.api.entity.HasBrand;
import com.ladbrokescoral.oxygen.cms.api.entity.SortableEntity;
import com.ladbrokescoral.oxygen.cms.api.service.validators.SegmentNamePattern;
import java.util.ArrayList;
import java.util.List;
import lombok.Data;
import lombok.EqualsAndHashCode;
import org.springframework.data.mongodb.core.mapping.Field;

@Data
@EqualsAndHashCode(callSuper = true)
public abstract class AbstractSegmentEntity extends SortableEntity
    implements SegmentEntity, HasBrand {

  private List<SegmentReference> segmentReferences = new ArrayList<>();
  private List<@SegmentNamePattern String> exclusionList = new ArrayList<>();
  private List<@SegmentNamePattern String> inclusionList = new ArrayList<>();
  private String archivalId;

  @Field(value = "applyUniversalSegments")
  private boolean universalSegment = Boolean.TRUE;

  private String message;
}
