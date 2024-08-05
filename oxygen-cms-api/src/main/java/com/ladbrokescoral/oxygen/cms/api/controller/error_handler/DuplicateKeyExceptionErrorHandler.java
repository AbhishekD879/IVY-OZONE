package com.ladbrokescoral.oxygen.cms.api.controller.error_handler;

import com.ladbrokescoral.oxygen.cms.api.controller.private_api.AbstractCrudController;
import java.util.Map;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import javax.servlet.http.HttpServletRequest;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.web.servlet.error.ErrorAttributes;
import org.springframework.dao.DuplicateKeyException;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.ControllerAdvice;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.ResponseBody;
import org.springframework.web.bind.annotation.ResponseStatus;

@ControllerAdvice(basePackageClasses = AbstractCrudController.class)
@Slf4j
public class DuplicateKeyExceptionErrorHandler extends AbstractErrorHandler {

  private static final String DUPLICATE_FIELD_PATTERN = "index: (.*?) ";
  private static final String SVGID_FIELD = "svgId";

  @Autowired
  public DuplicateKeyExceptionErrorHandler(ErrorAttributes errorAttributes) {
    super(errorAttributes);
  }

  @ExceptionHandler(DuplicateKeyException.class)
  @ResponseStatus(HttpStatus.BAD_REQUEST)
  @ResponseBody
  public Map<String, Object> validationError(DuplicateKeyException e, HttpServletRequest request) {
    String fieldName = extractNotUniqueFieldFromMessage(e.getMessage());
    return buildResponseEntity(
        request,
        HttpStatus.BAD_REQUEST.value(),
        "NotUniqueField",
        fieldName,
        String.format("Field %s must be unique", fieldName));
  }

  private String extractNotUniqueFieldFromMessage(String message) {
    Pattern pattern = Pattern.compile(DUPLICATE_FIELD_PATTERN);
    Matcher matcher = pattern.matcher(message);
    String notUniqueField = "";
    while (matcher.find()) {
      notUniqueField = matcher.group(1);
    }

    String[] fieldParts = notUniqueField.split("_");
    return fieldParts[fieldParts.length - 1].equals(SVGID_FIELD)
        ? fieldParts[fieldParts.length - 1]
        : fieldParts[0];
  }
}
