package com.ladbrokescoral.oxygen.cms.api.exception;

import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.ResponseStatus;

@ResponseStatus(
    value = HttpStatus.CONFLICT,
    reason = "Coupon Or Market Switcher widget exists and is enabled")
public class CouponAndMarketSwitcherCreateException extends RuntimeException {
  public CouponAndMarketSwitcherCreateException() {
    super();
  }
}
