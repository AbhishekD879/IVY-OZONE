package com.ladbrokescoral.oxygen.cms.api.dto;

import lombok.Data;

@Data
public class InplaySportDto extends AbstractSegmentDto {
  private int sportNumber;
  private int eventCount;
  private String categoryId;
  private Double displayOrder;
  private String sportName;
}
