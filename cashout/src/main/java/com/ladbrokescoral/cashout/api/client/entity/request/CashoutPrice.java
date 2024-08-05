package com.ladbrokescoral.cashout.api.client.entity.request;

import lombok.Builder;
import lombok.Data;

@Data
@Builder
public class CashoutPrice {
  private String num;
  private String den;
}
