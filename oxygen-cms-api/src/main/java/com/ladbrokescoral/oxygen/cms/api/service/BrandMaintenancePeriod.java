package com.ladbrokescoral.oxygen.cms.api.service;

import static java.lang.Long.max;
import static java.lang.Long.min;

import java.util.UUID;
import lombok.Data;
import lombok.EqualsAndHashCode;

@Data
@EqualsAndHashCode(onlyExplicitlyIncluded = true)
class BrandMaintenancePeriod {
  @EqualsAndHashCode.Include private String id = UUID.randomUUID().toString();
  private String brand;
  private long start;
  private long end;

  public void extend(BrandMaintenancePeriod newMaintenancePeriod) {
    this.setStart(min(this.getStart(), newMaintenancePeriod.getStart()));
    this.setEnd(max(this.getEnd(), newMaintenancePeriod.getEnd()));
  }
}
