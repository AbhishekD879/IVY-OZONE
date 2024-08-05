package com.ladbrokescoral.oxygen.cms.api.controller.error_handler;

import com.ladbrokescoral.oxygen.cms.api.controller.private_api.AbstractCrudController;
import com.ladbrokescoral.oxygen.cms.api.exception.InputValueIncorrectException;
import java.text.MessageFormat;
import java.util.Map;
import javax.servlet.http.HttpServletRequest;
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
public class InputValueIncorrectExceptionErrorHandler extends AbstractErrorHandler {

  private static final String MESSAGE_TEMPLATE = "{0} {1} values are incorrect";

  @Autowired
  public InputValueIncorrectExceptionErrorHandler(ErrorAttributes errorAttributes) {
    super(errorAttributes);
  }

  @ExceptionHandler(InputValueIncorrectException.class)
  @ResponseStatus(HttpStatus.BAD_REQUEST)
  @ResponseBody
  public Map<String, Object> validationError(
      InputValueIncorrectException e, HttpServletRequest request) {
    String message = MessageFormat.format(MESSAGE_TEMPLATE, e.getFieldName(), e.getValue());
    return buildResponseEntity(
        request, HttpStatus.BAD_REQUEST.value(), "IncorrectInputValue", e.getFieldName(), message);
  }
}
