package com.ladbrokescoral.oxygen.cms.api.dto;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.ToString;

@Data
@AllArgsConstructor
@NoArgsConstructor
@ToString
public class SiteServeEventExtendedDto {
  private String id;
  private String name;
  private String nameOverride;
  private String startTime;
  private Integer displayOrder;
  private boolean outright;
  private String categoryId;
  private String categoryCode;
  private String eventSortCode;
  private String templateMarketName;
}
