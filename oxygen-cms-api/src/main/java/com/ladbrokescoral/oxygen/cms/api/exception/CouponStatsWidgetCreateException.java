package com.ladbrokescoral.oxygen.cms.api.exception;

import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.ResponseStatus;

@ResponseStatus(value = HttpStatus.CONFLICT, reason = "Coupon stats widget exists and is enabled")
public class CouponStatsWidgetCreateException extends RuntimeException {
  public CouponStatsWidgetCreateException() {
    super();
  }
}
