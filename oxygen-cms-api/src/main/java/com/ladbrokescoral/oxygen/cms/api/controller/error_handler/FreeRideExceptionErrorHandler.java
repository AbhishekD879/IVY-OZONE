package com.ladbrokescoral.oxygen.cms.api.controller.error_handler;

import com.ladbrokescoral.oxygen.cms.api.controller.private_api.AbstractCrudController;
import com.ladbrokescoral.oxygen.cms.api.dto.ErrorResponseDto;
import com.ladbrokescoral.oxygen.cms.api.exception.CampaignAlreadyExistException;
import com.ladbrokescoral.oxygen.cms.api.exception.DeleteCampaignException;
import com.ladbrokescoral.oxygen.cms.api.exception.FreeRideException;
import com.ladbrokescoral.oxygen.cms.api.exception.FreeRideSplashPageFailureException;
import com.ladbrokescoral.oxygen.cms.api.exception.PotCreationException;
import com.ladbrokescoral.oxygen.cms.api.exception.UnauthorizedException;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.web.servlet.error.ErrorAttributes;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;

@RestControllerAdvice(basePackageClasses = AbstractCrudController.class)
@Slf4j
public class FreeRideExceptionErrorHandler extends AbstractErrorHandler {

  @Autowired
  public FreeRideExceptionErrorHandler(ErrorAttributes errorAttributes) {
    super(errorAttributes);
  }

  @ExceptionHandler({
    CampaignAlreadyExistException.class,
    PotCreationException.class,
    FreeRideSplashPageFailureException.class,
    DeleteCampaignException.class,
    FreeRideException.class
  })
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
