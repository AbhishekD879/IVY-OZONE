package com.ladbrokescoral.oxygen.cms.api.dto;

import com.ladbrokescoral.oxygen.cms.api.entity.PageType;
import com.ladbrokescoral.oxygen.cms.api.entity.RacingModuleConfig;
import com.ladbrokescoral.oxygen.cms.api.entity.SportModuleType;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class RacingModuleDto implements SportPageModuleDataItem {

  private Integer sportId;
  private String title;
  private boolean active;
  private RacingModuleConfig racingConfig;

  @Override
  public SportPageId sportPageId() {
    return new SportPageId(
        String.valueOf(sportId), PageType.sport, SportModuleType.RACING_MODULE, title);
  }
}
