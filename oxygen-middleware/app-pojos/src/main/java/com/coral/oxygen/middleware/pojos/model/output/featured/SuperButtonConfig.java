package com.coral.oxygen.middleware.pojos.model.output.featured;

import com.coral.oxygen.middleware.pojos.model.cms.featured.SuperButton;
import com.coral.oxygen.middleware.pojos.model.output.AbstractModuleData;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.google.gson.annotations.SerializedName;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.NoArgsConstructor;

@Data
@EqualsAndHashCode(callSuper = true)
@NoArgsConstructor
public class SuperButtonConfig extends AbstractModuleData {
  @SerializedName("@type")
  @JsonProperty("@type")
  private String type = "SuperButtonConfig";

  private Integer pageId;

  public SuperButtonConfig(SuperButton superButton) {
    this.pageId = superButton.getSportId();

    this.pageType = superButton.getPageType();
  }
}
