package com.coral.oxygen.middleware.pojos.model.cms;

import com.fasterxml.jackson.annotation.JsonProperty;
import com.google.gson.annotations.SerializedName;
import lombok.Data;

@Data
public class Tab {
  @SerializedName("tab-live")
  @JsonProperty("tab-live")
  private TabDetails tabLive;

  @SerializedName("tab-matches")
  @JsonProperty("tab-matches")
  private TabDetails tabMatches;

  @SerializedName("tab-outrights")
  @JsonProperty("tab-outrights")
  private TabDetails tabOutrights;

  @SerializedName("tab-specials")
  @JsonProperty("tab-specials")
  private TabDetails tabSpecials;
}
