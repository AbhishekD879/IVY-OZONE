package com.ladbrokescoral.oxygen.trendingbets.liveserv.domain;

import com.fasterxml.jackson.annotation.JsonSetter;
import java.util.Optional;
import lombok.Data;
import lombok.EqualsAndHashCode;

@EqualsAndHashCode
@Data
public class SelectionStatus implements AbstractStatus {

  private String status; // "status": "A" or "S"
  private Boolean settled; // "settled": "Y" or "N"
  private String displayed; // "displayed": "Y" or "N",
  private Integer priceNum; // "lp_num": "43",
  private Integer priceDen; // "lp_den": "1", price 43/1

  private boolean isPriceBoost;

  @JsonSetter("status")
  private void setStatus(String status) {
    this.status = status;
  }

  @JsonSetter("settled")
  private void setSettled(String settled) {
    this.settled = "Y".equals(settled);
  }

  @JsonSetter("displayed")
  private void setDisplayed(String displayed) {
    this.displayed = displayed;
  }

  @JsonSetter("lp_num")
  private void setPriceNum(String priceNum) {
    this.priceNum = Optional.ofNullable(priceNum).map(Integer::valueOf).orElse(null);
  }

  @JsonSetter("lp_den")
  private void setPriceDen(String priceDen) {
    this.priceDen = Optional.ofNullable(priceDen).map(Integer::valueOf).orElse(null);
  }

  @JsonSetter("stream_type")
  private void setIsPriceBoost(String priceType) {
    this.isPriceBoost = "PRICE_BOOST".equals(priceType);
  }
}
