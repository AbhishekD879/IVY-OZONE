package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import com.ladbrokescoral.oxygen.cms.api.service.public_api.NextRacesPublicService;
import java.io.IOException;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class NextRacesApi implements Public {

  private final NextRacesPublicService service;

  public NextRacesApi(NextRacesPublicService service) {
    this.service = service;
  }

  @GetMapping(value = "{brand}/upcell", produces = MediaType.APPLICATION_JSON_VALUE)
  public ResponseEntity nextRaces(@PathVariable("brand") String brand) throws IOException {
    return new ResponseEntity<>(service.find(brand), HttpStatus.OK);
  }
}
