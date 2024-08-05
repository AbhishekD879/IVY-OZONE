package com.ladbrokescoral.oxygen.cms.api.controller.error_handler;

import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;
import javax.servlet.http.HttpServletRequest;
import org.springframework.boot.web.error.ErrorAttributeOptions;
import org.springframework.boot.web.servlet.error.ErrorAttributes;
import org.springframework.validation.ObjectError;
import org.springframework.web.context.request.ServletWebRequest;
import org.springframework.web.context.request.WebRequest;

// FIXME: need rework -- use AbstractErrorController and ResponseEntityExceptionHandler
public abstract class AbstractErrorHandler {

  private final ErrorAttributes errorAttributes;

  public AbstractErrorHandler(ErrorAttributes errorAttributes) {
    this.errorAttributes = errorAttributes;
  }

  protected Map<String, Object> buildResponseEntity(
      HttpServletRequest request,
      int httpStatusCode,
      String code,
      String field,
      String defaultMessage) {

    WebRequest servletWebRequest = new ServletWebRequest(request);

    Map<String, Object> responseErrorAttributes =
        this.errorAttributes.getErrorAttributes(
            servletWebRequest, ErrorAttributeOptions.defaults());

    HashMap<String, String> attributes = new HashMap<>();
    attributes.put("code", field);

    ObjectError error =
        new ObjectError("", new String[] {code}, new Object[] {attributes}, defaultMessage);
    responseErrorAttributes.put("errors", Arrays.asList(error));
    responseErrorAttributes.put("status", httpStatusCode);

    return responseErrorAttributes;
  }
}
