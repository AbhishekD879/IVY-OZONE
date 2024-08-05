package com.ladbrokescoral.oxygen.bigcompetition.exception;

import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.ResponseStatus;

@ResponseStatus(value = HttpStatus.NOT_FOUND, reason = "Element not found")
public class NotFoundException extends RuntimeException {}
