package com.oxygen.publisher.model;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class TabDetails {
  @JsonProperty("tablabel")
  private String tabLabel;

  private Boolean visible;

  @Override
  public String toString() {
    final StringBuilder sb = new StringBuilder("TabDetails{");
    sb.append("tabLabel='").append(tabLabel).append('\'');
    sb.append(", visible=").append(visible);
    sb.append('}');
    return sb.toString();
  }
}
