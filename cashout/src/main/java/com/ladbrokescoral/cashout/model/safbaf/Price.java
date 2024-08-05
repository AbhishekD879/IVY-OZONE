package com.ladbrokescoral.cashout.model.safbaf;

import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonInclude.Include;
import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Data;

@Data
public class Price {
  private String channel;
  private String selectionPriceType;
  private String region;
  private Double decimalPrice;
  private Integer numPrice;
  private Integer denPrice;
  private Boolean isInitial;

  @JsonProperty("ps_den")
  @JsonInclude(value = Include.NON_NULL, content = Include.NON_EMPTY)
  private String psDen;

  @JsonProperty("ps_num")
  @JsonInclude(value = Include.NON_NULL, content = Include.NON_EMPTY)
  private String psNum;

  @JsonInclude(value = Include.NON_NULL, content = Include.NON_EMPTY)
  private String status;

  @JsonInclude(value = Include.NON_NULL, content = Include.NON_EMPTY)
  @JsonProperty("stream_type")
  private String priceStreamType;
}
