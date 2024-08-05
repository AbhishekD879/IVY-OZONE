package com.ladbrokescoral.oxygen.cms.api.dto;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class SiteServeEventDto {
  private String id;
  private String categoryId;
  private Integer marketCount;
  private String name;
  private String nameOverride;
  private boolean outright;
}
