package com.ladbrokescoral.oxygen.cms.api.controller.error_handler;

import com.ladbrokescoral.oxygen.cms.api.controller.private_api.AbstractCrudController;
import com.ladbrokescoral.oxygen.cms.api.dto.ErrorResponseDto;
import com.ladbrokescoral.oxygen.cms.api.exception.*;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.web.servlet.error.ErrorAttributes;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestControllerAdvice;

@RestControllerAdvice(basePackageClasses = AbstractCrudController.class)
@Slf4j
public class BetPackExceptionErrorHandler extends AbstractErrorHandler {

  @Autowired
  public BetPackExceptionErrorHandler(ErrorAttributes errorAttributes) {
    super(errorAttributes);
  }

  @ExceptionHandler({BetPackMarketPlaceException.class})
  @ResponseStatus(HttpStatus.INTERNAL_SERVER_ERROR)
  public ErrorResponseDto handleInternalServerException(Exception e) {
    log.error("Internal Server Error", e);
    return new ErrorResponseDto(e.getMessage());
  }

  @ExceptionHandler(UnauthorizedException.class)
  @ResponseStatus(HttpStatus.UNAUTHORIZED)
  public ErrorResponseDto internalServerError(UnauthorizedException e) {
    log.error("Unauthorized Error", e);
    return new ErrorResponseDto(e.getMessage());
  }
}
