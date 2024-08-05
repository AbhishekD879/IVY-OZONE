package com.ladbrokescoral.oxygen.cms.api.dto;

import com.fasterxml.jackson.annotation.JsonIgnore;
import com.ladbrokescoral.oxygen.cms.api.entity.AbstractSportEntity;
import com.ladbrokescoral.oxygen.cms.api.entity.PageType;
import com.ladbrokescoral.oxygen.cms.api.entity.SportModuleType;
import lombok.EqualsAndHashCode;
import lombok.ToString;

@ToString
@EqualsAndHashCode
public abstract class BaseModularContentDto implements SportPageModuleDataItem {

  @JsonIgnore
  protected SportPageId sportPageId =
      new SportPageId(
          AbstractSportEntity.SPORT_HOME_PAGE, PageType.sport, SportModuleType.FEATURED);

  @Override
  public SportPageId sportPageId() {
    return sportPageId;
  }

  public BaseModularContentDto sportPageId(SportPageId sportPageId) {
    this.sportPageId = sportPageId;
    return this;
  }
}
