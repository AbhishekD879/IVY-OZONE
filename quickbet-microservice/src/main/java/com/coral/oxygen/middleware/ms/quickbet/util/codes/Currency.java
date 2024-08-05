package com.coral.oxygen.middleware.ms.quickbet.util.codes;

import lombok.AllArgsConstructor;
import lombok.Getter;

@AllArgsConstructor
@Getter
public enum Currency {
  USD("USD"),
  GBP("GBP");

  private String code;
}
