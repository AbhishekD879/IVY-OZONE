package com.ladbrokescoral.cashout.model.response;

import com.ladbrokescoral.cashout.model.Code;
import lombok.AllArgsConstructor;
import lombok.Data;

@Data
@AllArgsConstructor
public class ErrorBetResponse implements BetResponse {
  private Error error;

  public static ErrorBetResponse create(Code code) {
    return new ErrorBetResponse(new Error(code));
  }

  @Data
  @AllArgsConstructor
  public static class Error {
    private Code code;
  }
}
