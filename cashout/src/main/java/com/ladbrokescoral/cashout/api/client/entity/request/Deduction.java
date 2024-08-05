package com.ladbrokescoral.cashout.api.client.entity.request;

import lombok.Builder;
import lombok.Data;

@Data
@Builder
public class Deduction {
  private String type;
  private String num;
  private String den;
}
