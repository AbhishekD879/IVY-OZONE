package com.ladbrokescoral.oxygen.betpackmp.controller;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

/** Created by Rakesh Bonu on 26.07.22. */
@RestController
public final class HealthController {

  @GetMapping("/health")
  public ResponseEntity<String> getHealth() {
    HttpStatus httpStatus = HttpStatus.OK;
    return new ResponseEntity<>("Health check status ", httpStatus);
  }
}
