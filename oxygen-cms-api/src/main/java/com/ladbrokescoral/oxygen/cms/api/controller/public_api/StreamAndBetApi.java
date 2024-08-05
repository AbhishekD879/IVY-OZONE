package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import com.ladbrokescoral.oxygen.cms.api.service.public_api.StreamAndBetPublicService;
import java.util.Collections;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class StreamAndBetApi implements Public {

  private final StreamAndBetPublicService service;

  public StreamAndBetApi(StreamAndBetPublicService service) {
    this.service = service;
  }

  @GetMapping("{brand}/stream-and-bet")
  public ResponseEntity findByBrand(@PathVariable("brand") String brand) {
    return service
        .findByBrand(brand)
        .map(ResponseEntity::ok)
        .orElseGet(() -> new ResponseEntity<>(Collections.emptyList(), HttpStatus.OK));
  }
}
