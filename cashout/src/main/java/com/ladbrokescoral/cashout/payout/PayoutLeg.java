package com.ladbrokescoral.cashout.payout;

import com.fasterxml.jackson.annotation.JsonIgnore;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonInclude.Include;
import java.util.List;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class PayoutLeg {

  @JsonIgnore private String id;

  @JsonInclude(value = Include.NON_NULL, content = Include.NON_EMPTY)
  private String result;

  @JsonInclude(value = Include.NON_NULL, content = Include.NON_EMPTY)
  private String priceType;

  @JsonInclude(value = Include.NON_NULL, content = Include.NON_EMPTY)
  private PayoutPrice strikePrice;

  @JsonInclude(value = Include.NON_NULL, content = Include.NON_EMPTY)
  private PayoutPrice startingPrice;

  @JsonInclude(value = Include.NON_NULL, content = Include.NON_EMPTY)
  private PayoutPrice eachWayFactor;

  @JsonInclude(value = Include.NON_NULL, content = Include.NON_EMPTY)
  private List<Deduction> deductions;
}
