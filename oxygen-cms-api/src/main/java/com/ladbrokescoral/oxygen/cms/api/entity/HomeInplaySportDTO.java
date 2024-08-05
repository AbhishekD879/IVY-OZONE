package com.ladbrokescoral.oxygen.cms.api.entity;

import com.ladbrokescoral.oxygen.cms.api.entity.segment.AbstractSegmentEntity;
import com.ladbrokescoral.oxygen.cms.api.service.validators.Brand;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@AllArgsConstructor
@NoArgsConstructor
@Builder
public class HomeInplaySportDTO extends AbstractSegmentEntity {

  private int eventCount;
  private String categoryId;
  private String tier;
  private String sportName;
  private int sportNumber;
  @Brand protected String brand;
}
