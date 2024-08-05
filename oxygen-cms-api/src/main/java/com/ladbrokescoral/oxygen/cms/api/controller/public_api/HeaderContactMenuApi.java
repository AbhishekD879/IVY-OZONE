package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import com.ladbrokescoral.oxygen.cms.api.service.public_api.HeaderContactMenuPublicService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class HeaderContactMenuApi implements Public {

  private final HeaderContactMenuPublicService service;

  @Autowired
  public HeaderContactMenuApi(HeaderContactMenuPublicService service) {
    this.service = service;
  }

  @GetMapping(value = "{brand}/header-contact-menu")
  public ResponseEntity findByBrand(@PathVariable("brand") String brand) {
    return new ResponseEntity<>(service.find(brand), HttpStatus.OK);
  }
}
