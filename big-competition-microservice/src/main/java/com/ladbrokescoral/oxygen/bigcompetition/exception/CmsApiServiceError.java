package com.ladbrokescoral.oxygen.bigcompetition.exception;

import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.ResponseStatus;

@ResponseStatus(value = HttpStatus.SERVICE_UNAVAILABLE, reason = "Error getting data from cms-api")
public class CmsApiServiceError extends RuntimeException {}
