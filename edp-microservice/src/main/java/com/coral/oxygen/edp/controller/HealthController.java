package com.coral.oxygen.edp.controller;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

/** Created by llegkyy on 03.10.17. */
@RestController
public final class HealthController {

  @GetMapping("/health")
  public ResponseEntity getHealth() {
    HttpStatus httpStatus = HttpStatus.OK;
    return new ResponseEntity("Health check status", httpStatus);
  }
}
