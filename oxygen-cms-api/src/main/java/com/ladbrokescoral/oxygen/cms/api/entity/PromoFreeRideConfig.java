package com.ladbrokescoral.oxygen.cms.api.entity;

import lombok.Data;

@Data
public class PromoFreeRideConfig {
  private Boolean isFreeRidePromo = false;
  private String errorMessage;
  private String ctaPreLoginTitle;
  private String ctaPostLoginTitle;
}
