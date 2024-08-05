package com.ladbrokescoral.oxygen.cms.api.dto;

import lombok.AllArgsConstructor;
import lombok.Data;

@Data
@AllArgsConstructor
public class PaymentMethodDto {
  private boolean active;
  private String name;
  private String identifier;
  private Double sortOrder;
}
