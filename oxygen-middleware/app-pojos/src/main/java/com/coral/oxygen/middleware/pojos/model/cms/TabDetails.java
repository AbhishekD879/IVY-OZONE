package com.coral.oxygen.middleware.pojos.model.cms;

import com.fasterxml.jackson.annotation.JsonProperty;
import com.google.gson.annotations.SerializedName;
import lombok.Data;

@Data
public class TabDetails {
  @SerializedName("tablabel")
  @JsonProperty("tablabel")
  private String tabLabel;

  private Boolean visible;
}
