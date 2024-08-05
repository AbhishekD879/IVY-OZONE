package com.ladbrokescoral.cashout.api.client.entity.request;

import java.util.List;
import lombok.Builder;
import lombok.Data;
import lombok.Singular;

@Data
@Builder
public class CashoutLeg {
  private String legNo;
  private String legSort;
  @Singular private List<CashoutPart> parts;
}
