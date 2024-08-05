package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import com.ladbrokescoral.oxygen.cms.api.service.public_api.SsoPagePublicService;
import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class SsoPageApi implements Public {

  private final SsoPagePublicService service;

  @Autowired
  public SsoPageApi(SsoPagePublicService service) {
    this.service = service;
  }

  @GetMapping(value = "{brand}/sso-page/{osType}")
  public ResponseEntity findByBrand(
      @PathVariable("brand") String brand, @PathVariable("osType") String osType) {
    List list = service.findByBrand(brand, osType);
    return new ResponseEntity<>(list, HttpStatus.OK);
  }
}
