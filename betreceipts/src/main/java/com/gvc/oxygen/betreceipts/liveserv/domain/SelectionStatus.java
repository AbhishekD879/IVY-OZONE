package com.gvc.oxygen.betreceipts.liveserv.domain;

import com.fasterxml.jackson.annotation.JsonSetter;
import java.util.Optional;
import lombok.Data;
import lombok.EqualsAndHashCode;
import org.apache.commons.lang3.math.NumberUtils;

@EqualsAndHashCode
@Data
public class SelectionStatus implements AbstractStatus {

  private Boolean active; // "status": "A" or "S"
  private Boolean settled; // "settled": "Y" or "N"
  private Boolean displayed; // "displayed": "Y" or "N",
  private Integer priceNum; // "lp_num": "43",
  private Integer priceDen; // "lp_den": "1", price 43/1

  @JsonSetter("status")
  private void setActive(String status) {
    this.active = "A".equals(status);
  }

  @JsonSetter("settled")
  private void setSettled(String settled) {
    this.settled = "Y".equals(settled);
  }

  @JsonSetter("displayed")
  private void setDisplayed(String displayed) {
    this.displayed = "Y".equals(displayed);
  }

  @JsonSetter("lp_num")
  private void setPriceNum(String priceNum) {
    this.priceNum = Optional.ofNullable(priceNum).map(NumberUtils::toInt).orElse(null);
  }

  @JsonSetter("lp_den")
  private void setPriceDen(String priceDen) {
    this.priceDen = Optional.ofNullable(priceDen).map(NumberUtils::toInt).orElse(null);
  }
}
