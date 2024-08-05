package com.ladbrokescoral.oxygen.cms.api.exception;

import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.ResponseStatus;

@ResponseStatus(
    value = HttpStatus.CONFLICT,
    reason = "Duplicate Insertion.. Similar Contents should not be created in same time range")
public class StatisticalContentNotUniqueException extends RuntimeException {}
