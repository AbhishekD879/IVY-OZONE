package com.oxygen.publisher.model;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class Tab {
  @JsonProperty("tab-live")
  private TabDetails tabLive;

  @JsonProperty("tab-matches")
  private TabDetails tabMatches;

  @JsonProperty("tab-outrights")
  private TabDetails tabOutrights;

  @JsonProperty("tab-specials")
  private TabDetails tabSpecials;

  @Override
  public String toString() {
    final StringBuilder sb = new StringBuilder("Tab{");
    sb.append("tabLive=").append(tabLive);
    sb.append(", tabMatches=").append(tabMatches);
    sb.append(", tabOutrights=").append(tabOutrights);
    sb.append(", tabSpecials=").append(tabSpecials);
    sb.append('}');
    return sb.toString();
  }
}
