package com.entain.oxygen.betbuilder_middleware.exception;

import java.text.SimpleDateFormat;
import java.util.HashMap;
import java.util.Map;
import org.springframework.boot.web.error.ErrorAttributeOptions;
import org.springframework.boot.web.reactive.error.DefaultErrorAttributes;
import org.springframework.stereotype.Component;
import org.springframework.web.reactive.function.server.ServerRequest;

@Component
public class GlobalErrorAttributes extends DefaultErrorAttributes {

  @Override
  public Map<String, Object> getErrorAttributes(
      ServerRequest request, ErrorAttributeOptions options) {
    Map<String, Object> map = new HashMap<>();
    Throwable ex = getError(request);

    map.put("path", request.path());
    map.put("errorMessage", ex.getMessage());
    map.put(
        "timestamp",
        new SimpleDateFormat("yyyy-MM-dd'T'hh:mm:ss.SSS").format(System.currentTimeMillis()));

    return map;
  }
}
