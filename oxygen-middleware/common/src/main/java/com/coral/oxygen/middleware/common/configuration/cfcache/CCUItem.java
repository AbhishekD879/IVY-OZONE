package com.coral.oxygen.middleware.common.configuration.cfcache;

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
