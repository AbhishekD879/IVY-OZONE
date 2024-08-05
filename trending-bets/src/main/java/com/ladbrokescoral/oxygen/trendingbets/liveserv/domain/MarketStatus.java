package com.ladbrokescoral.oxygen.trendingbets.liveserv.domain;

import com.fasterxml.jackson.annotation.JsonSetter;
import lombok.Data;
import lombok.EqualsAndHashCode;

@EqualsAndHashCode
@Data
public class MarketStatus implements AbstractStatus {

  private String status; // "status": "A" or "S"

  private String displayed; // "displayed": "Y" or "N",

  @JsonSetter("status")
  private void setStatus(String status) {
    this.status = status;
  }

  @JsonSetter("displayed")
  private void setDisplayed(String displayed) {
    this.displayed = displayed;
  }
}
