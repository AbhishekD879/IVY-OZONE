package com.ladbrokescoral.oxygen.cms.api.controller.error_handler;

import com.ladbrokescoral.oxygen.cms.api.controller.public_api.Public;
import com.ladbrokescoral.oxygen.cms.api.dto.ErrorResponseDto;
import com.ladbrokescoral.oxygen.cms.api.exception.*;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestControllerAdvice;

@RestControllerAdvice(basePackageClasses = Public.class)
@Slf4j
public class RssRewardExceptionErrorHandler {

  @ExceptionHandler({RssRewardNotFoundException.class})
  @ResponseStatus(HttpStatus.NOT_FOUND)
  public ErrorResponseDto handleRecordsNotFound(Exception e) {
    log.error("Records Not Found in CMS", e);
    return new ErrorResponseDto(e.getMessage());
  }
}
