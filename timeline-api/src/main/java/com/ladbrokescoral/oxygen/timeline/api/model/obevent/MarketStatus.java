package com.ladbrokescoral.oxygen.timeline.api.model.obevent;

import com.fasterxml.jackson.annotation.JsonSetter;
import lombok.Data;
import lombok.EqualsAndHashCode;

@EqualsAndHashCode(callSuper = true)
@Data
public class MarketStatus extends AbstractStatus {

  private Boolean active; // "status": "A" or "S"
  private Boolean displayed; // "displayed": "Y" or "N",
  private Boolean lpAvailable; //  "lp_avail": "Y",
  private Boolean spAvailable; //  "sp_avail": "Y",
  private Boolean marketBetInRun; // "bet_in_run": "Y"

  @JsonSetter("status")
  private void setActive(String status) {
    this.active = "A".equals(status);
  }

  @JsonSetter("displayed")
  private void setDisplayed(String displayed) {
    this.displayed = "Y".equals(displayed);
  }

  @JsonSetter("sp_avail")
  private void setSpAvailable(String spAvailable) {
    this.spAvailable = "Y".equals(spAvailable);
  }

  @JsonSetter("lp_avail")
  private void setLpAvailable(String lpAvailable) {
    this.lpAvailable = "Y".equals(lpAvailable);
  }

  @JsonSetter("bet_in_run")
  private void setMarketBetInRun(String betInRun) {
    this.marketBetInRun = "Y".equals(betInRun);
  }
}
