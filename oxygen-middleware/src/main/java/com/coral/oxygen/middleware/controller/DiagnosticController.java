package com.coral.oxygen.middleware.controller;

import com.coral.oxygen.middleware.common.service.ErrorsStorageService;
import com.coral.oxygen.middleware.util.PropertyUtils;
import java.util.Map;
import java.util.Properties;
import lombok.RequiredArgsConstructor;
import org.springframework.core.env.Environment;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

/** Created by azayats on 07.02.17. */
@RequiredArgsConstructor
@RestController
@RequestMapping(value = "/api/diagnostic")
public class DiagnosticController {

  private final Environment environment;

  private final ErrorsStorageService errorsStorageService;

  @GetMapping
  public Properties config() {
    return PropertyUtils.getProperties(environment);
  }

  @GetMapping("/errors")
  public Map<String, Object> errors() {
    return errorsStorageService.getErrors();
  }
}
