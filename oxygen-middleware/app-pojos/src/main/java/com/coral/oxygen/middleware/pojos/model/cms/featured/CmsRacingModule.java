package com.coral.oxygen.middleware.pojos.model.cms.featured;

import lombok.Data;
import lombok.EqualsAndHashCode;

@Data
@EqualsAndHashCode(callSuper = true)
public class CmsRacingModule extends SportPageModuleDataItem {
  private String id;
  private Integer sportId;
  private boolean active;
  private RacingConfig racingConfig;
}
