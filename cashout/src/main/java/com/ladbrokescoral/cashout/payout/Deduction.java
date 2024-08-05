package com.ladbrokescoral.cashout.payout;

import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonInclude.Include;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class Deduction {
  @JsonInclude(value = Include.NON_NULL, content = Include.NON_EMPTY)
  private DeductionDetails deductionDetail;

  @JsonInclude(value = Include.NON_NULL, content = Include.NON_EMPTY)
  private String deductionType;
}
