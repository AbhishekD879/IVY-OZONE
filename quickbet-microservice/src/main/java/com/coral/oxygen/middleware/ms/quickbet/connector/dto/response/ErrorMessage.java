package com.coral.oxygen.middleware.ms.quickbet.connector.dto.response;

import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
public final class ErrorMessage {
  private String code;
  private int subErrorCode;
  private String message;

  public ErrorMessage(int code, String message) {
    this.code = String.valueOf(code);
    this.message = message;
  }

  public ErrorMessage(String code, String message) {
    this.code = code;
    this.message = message;
  }

  public ErrorMessage(String code, int subErrorCode, String message) {
    this.code = code;
    this.subErrorCode = subErrorCode;
    this.message = message;
  }
}
