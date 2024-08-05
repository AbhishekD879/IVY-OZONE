package com.ladbrokescoral.cashout.payout;

import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonInclude.Include;
import com.fasterxml.jackson.annotation.JsonProperty;
import java.util.List;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class PayoutRequest {

  @JsonProperty("betNo")
  private String betId;

  @JsonInclude(value = Include.NON_NULL, content = Include.NON_EMPTY)
  private String stake;

  @JsonInclude(value = Include.NON_NULL, content = Include.NON_EMPTY)
  private String tokenValue;

  @JsonInclude(value = Include.NON_NULL, content = Include.NON_EMPTY)
  private String betType;

  @JsonInclude(value = Include.NON_NULL, content = Include.NON_EMPTY)
  private String legType;

  @JsonInclude(value = Include.NON_NULL, content = Include.NON_EMPTY)
  private String foldSize;

  @JsonInclude(value = Include.NON_NULL, content = Include.NON_EMPTY)
  private List<PayoutLeg> legs;
}
