package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import com.ladbrokescoral.oxygen.cms.api.dto.StaticBlockDto;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.StaticBlockPublicService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class StaticBlockApi implements Public {

  private final StaticBlockPublicService service;

  @Autowired
  public StaticBlockApi(StaticBlockPublicService service) {
    this.service = service;
  }

  @GetMapping(value = "{brand}/static-block/{uri}")
  public ResponseEntity findByBrandAndUri(
      @PathVariable("brand") String brand, @PathVariable("uri") String uri) {
    return service
        .find(brand, uri)
        .map(ResponseEntity::ok)
        .orElseGet(() -> ResponseEntity.ok(new StaticBlockDto()));
  }
}
