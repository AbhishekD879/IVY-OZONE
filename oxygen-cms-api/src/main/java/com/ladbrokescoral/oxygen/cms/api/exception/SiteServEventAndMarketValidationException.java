package com.ladbrokescoral.oxygen.cms.api.exception;

import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.ResponseStatus;

@ResponseStatus(
    value = HttpStatus.INTERNAL_SERVER_ERROR,
    reason = "Event With Market Hierarchy Does not Exist in OB")
public class SiteServEventAndMarketValidationException extends RuntimeException {}
