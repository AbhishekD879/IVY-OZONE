package com.ladbrokescoral.oxygen.cms.api.controller.error_handler;

import com.ladbrokescoral.oxygen.cms.api.constants.FZConstants;
import com.ladbrokescoral.oxygen.cms.api.controller.private_api.AbstractCrudController;
import com.ladbrokescoral.oxygen.cms.api.exception.FanzoneSycCreateException;
import com.ladbrokescoral.oxygen.cms.api.exception.InvalidPageNameException;
import com.ladbrokescoral.oxygen.cms.api.exception.InvalidTeamIdException;
import com.ladbrokescoral.oxygen.cms.api.exception.PreferenceCentreCreateException;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.web.servlet.error.ErrorAttributes;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.ControllerAdvice;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.ResponseStatus;

@ControllerAdvice(basePackageClasses = AbstractCrudController.class)
@Slf4j
public class FanzonesExceptionErrorHandler extends AbstractErrorHandler {
  @Autowired
  public FanzonesExceptionErrorHandler(ErrorAttributes errorAttributes) {
    super(errorAttributes);
  }

  @ResponseStatus(value = HttpStatus.NOT_FOUND, reason = FZConstants.INVALID_PAGENAME)
  @ExceptionHandler(InvalidPageNameException.class)
  public void handleInvalidPageNameException(InvalidPageNameException e) {
    // Do nothing
  }

  @ResponseStatus(value = HttpStatus.NOT_FOUND, reason = FZConstants.INVALID_TEAMID)
  @ExceptionHandler(InvalidTeamIdException.class)
  public void handleInvalidTeamIdException(InvalidTeamIdException e) {
    // Do nothing
  }

  @ResponseStatus(value = HttpStatus.NOT_FOUND, reason = FZConstants.FANZONESYC_ALREADYEXIST)
  @ExceptionHandler(FanzoneSycCreateException.class)
  public void handleFanzoneSycCreateException(FanzoneSycCreateException e) {
    // Do nothing
  }

  @ResponseStatus(value = HttpStatus.NOT_FOUND, reason = FZConstants.PREFERENCECENTRE_ALREADYEXIST)
  @ExceptionHandler(PreferenceCentreCreateException.class)
  public void handlePreferenceCentreCreateException(PreferenceCentreCreateException e) {
    // Do nothing
  }
}
