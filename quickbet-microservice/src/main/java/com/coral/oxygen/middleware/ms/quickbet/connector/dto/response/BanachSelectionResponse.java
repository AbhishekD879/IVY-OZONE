package com.coral.oxygen.middleware.ms.quickbet.connector.dto.response;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class BanachSelectionResponse {
  private FractionalPriceDto data;
  private String roomName;
}
