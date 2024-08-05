package com.coral.oxygen.middleware.ms.quickbet.util.codes;

import lombok.AllArgsConstructor;
import lombok.Getter;

@AllArgsConstructor
@Getter
public enum StatusResponse {
  UNKNOWN("unknown"),
  SUCCESS("success");

  private String message;
}
