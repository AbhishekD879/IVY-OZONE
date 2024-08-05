package com.ladbrokescoral.oxygen.cms.api.entity;

import static com.ladbrokescoral.oxygen.cms.api.mapping.RacingModuleType.VIRTUAL_RACE_CAROUSEL;

import javax.validation.constraints.Pattern;
import lombok.Data;
import lombok.EqualsAndHashCode;
import org.hibernate.validator.constraints.Range;

@Data
@EqualsAndHashCode(callSuper = true)
public class VirtualRacingCarouselModuleConfig extends RacingModuleConfig {

  @Range(min = 1, max = 12)
  private int limit = 5;

  @Pattern(message = "Comma separated integers are allowed", regexp = "^(\\d)+(,\\s*\\d+)*$")
  private String excludeTypeIds;

  @Range(min = 1)
  private int classId;

  public VirtualRacingCarouselModuleConfig() {
    super();
    setType(VIRTUAL_RACE_CAROUSEL);
  }
}
