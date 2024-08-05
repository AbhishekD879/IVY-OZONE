package com.ladbrokescoral.oxygen.cms.api.dto;

import java.time.Instant;
import lombok.Data;
import lombok.EqualsAndHashCode;

@Data
@EqualsAndHashCode(callSuper = false)
public class SegmentReferenceDto {
  private String segment;
  private Double displayOrder;
  private Instant updatedAt;
  private String pageRefId;
}
