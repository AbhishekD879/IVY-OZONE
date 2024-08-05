package com.ladbrokescoral.oxygen.cms.api.exception;

import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.ResponseStatus;

@ResponseStatus(
    value = HttpStatus.UNPROCESSABLE_ENTITY,
    reason = "JWT validity cannot be asserted and should not be trusted")
public class InvalidJwtException extends RuntimeException {

  private static final long serialVersionUID = 7567237274269629943L;
}
