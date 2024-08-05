package com.ladbrokescoral.oxygen.cms.api.entity;

import static com.ladbrokescoral.oxygen.cms.api.mapping.RacingModuleType.INTERNATIONAL_TOTE_CAROUSEL;

import javax.validation.constraints.Min;
import lombok.Data;
import lombok.EqualsAndHashCode;

@Data
@EqualsAndHashCode(callSuper = true)
public class InternationalToteConfig extends RacingModuleConfig {

  @Min(1)
  private int classId = 802;

  private int timeRangeHours = 24;

  public InternationalToteConfig() {
    super();
    setType(INTERNATIONAL_TOTE_CAROUSEL);
  }
}
