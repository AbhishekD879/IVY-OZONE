package com.ladbrokescoral.oxygen.cms.api.controller.error_handler;

import com.ladbrokescoral.oxygen.cms.api.controller.private_api.AbstractCrudController;
import com.ladbrokescoral.oxygen.cms.api.exception.GameCreationException;
import com.ladbrokescoral.oxygen.cms.api.exception.SeasonAlreadyExistException;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.web.servlet.error.ErrorAttributes;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.ControllerAdvice;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.ResponseBody;
import org.springframework.web.bind.annotation.ResponseStatus;

@ControllerAdvice(basePackageClasses = AbstractCrudController.class)
@Slf4j
public class OneTwoFreeErrorHandler extends AbstractErrorHandler {

  @Autowired
  public OneTwoFreeErrorHandler(ErrorAttributes errorAttributes) {
    super(errorAttributes);
  }

  @ExceptionHandler({SeasonAlreadyExistException.class, GameCreationException.class})
  @ResponseStatus(HttpStatus.INTERNAL_SERVER_ERROR)
  @ResponseBody
  public ResponseDto handleInternalServerException(Exception e) {
    log.error("Internal Server Error", e);
    return new ResponseDto(e.getMessage());
  }

  @Data
  @AllArgsConstructor
  public static class ResponseDto {
    private String message;
  }
}
