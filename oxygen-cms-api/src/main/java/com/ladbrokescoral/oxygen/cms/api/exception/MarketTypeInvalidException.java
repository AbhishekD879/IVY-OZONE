package com.ladbrokescoral.oxygen.cms.api.exception;

import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.ResponseStatus;

@ResponseStatus(
    value = HttpStatus.CONFLICT,
    reason = "Market Type is not Valid for the given Brand")
public class MarketTypeInvalidException extends RuntimeException {}
