package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import com.ladbrokescoral.oxygen.cms.api.service.public_api.SportsFeaturedTabPublicService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class SportsFeaturedTabApi implements Public {
  private final SportsFeaturedTabPublicService service;

  @Autowired
  public SportsFeaturedTabApi(SportsFeaturedTabPublicService service) {
    this.service = service;
  }

  @GetMapping("{brand}/sports-featured-tab/{path}")
  public ResponseEntity getFeatureTabByPath(@PathVariable String brand, @PathVariable String path) {
    return service
        .getFeatureTabByPath(brand, path)
        .map(ResponseEntity::ok)
        .orElseGet(() -> new ResponseEntity<>(HttpStatus.NOT_FOUND));
  }
}
