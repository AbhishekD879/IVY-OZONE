package com.ladbrokescoral.oxygen.cms.api.entity;

import lombok.Builder;
import lombok.Data;
import lombok.EqualsAndHashCode;

@Data
@Builder
@EqualsAndHashCode
public class CCUItem {
  private String brand;
  private String path;
  private String name;
  private String cacheTag;
}
