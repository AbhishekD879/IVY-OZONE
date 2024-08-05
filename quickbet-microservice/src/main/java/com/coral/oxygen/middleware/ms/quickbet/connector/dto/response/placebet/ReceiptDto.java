package com.coral.oxygen.middleware.ms.quickbet.connector.dto.response.placebet;

import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
public class ReceiptDto {

  private String id;

  public ReceiptDto withId(String id) {
    this.id = id;
    return this;
  }
}
