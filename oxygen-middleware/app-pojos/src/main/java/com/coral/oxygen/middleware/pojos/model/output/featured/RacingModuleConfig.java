package com.coral.oxygen.middleware.pojos.model.output.featured;

import com.coral.oxygen.middleware.pojos.model.ChangeDetect;
import com.coral.oxygen.middleware.pojos.model.cms.featured.CmsRacingModule;
import com.coral.oxygen.middleware.pojos.model.output.AbstractModuleData;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.google.gson.annotations.SerializedName;
import lombok.*;

@Data
@EqualsAndHashCode(callSuper = true)
@NoArgsConstructor
public class RacingModuleConfig extends AbstractModuleData {

  @SerializedName("@type")
  @JsonProperty("@type")
  private String type = "RacingModuleConfig";

  @Getter private String id;

  private String name;
  private boolean active;

  public RacingModuleConfig(CmsRacingModule cmsRacingModule) {
    this.id = cmsRacingModule.getId();
    this.name = cmsRacingModule.getRacingConfig().getAbbreviation();
    this.active = cmsRacingModule.isActive();
    this.pageType = cmsRacingModule.getPageType();
  }

  @ChangeDetect
  public String getName() {
    return name;
  }

  @Override
  public String idForChangeDetection() {
    return id;
  }
}
