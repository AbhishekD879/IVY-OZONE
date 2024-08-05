package com.coral.oxygen.middleware.ms.quickbet.connector.dto;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@Builder
@AllArgsConstructor
public class FreeBetRequest {
  private Long id;
  private String stake;
  private boolean oddsBoost;
}
