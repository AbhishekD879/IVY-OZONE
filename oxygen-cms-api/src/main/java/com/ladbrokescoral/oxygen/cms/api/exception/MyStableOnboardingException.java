package com.ladbrokescoral.oxygen.cms.api.exception;

import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.ResponseStatus;

@ResponseStatus(
    value = HttpStatus.INTERNAL_SERVER_ERROR,
    reason = "Invalid operation in MyStable onboarding ")
public class MyStableOnboardingException extends RuntimeException {
  public MyStableOnboardingException(String msg) {
    super(msg);
  }
}
