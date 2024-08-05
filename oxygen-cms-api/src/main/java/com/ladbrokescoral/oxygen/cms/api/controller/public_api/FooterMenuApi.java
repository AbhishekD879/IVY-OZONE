package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import com.ladbrokescoral.oxygen.cms.api.dto.FooterMenuV2Dto;
import com.ladbrokescoral.oxygen.cms.api.dto.FooterMenuV3Dto;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.FooterMenuPublicService;
import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.util.CollectionUtils;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class FooterMenuApi implements Public {

  private final FooterMenuPublicService service;

  @Autowired
  public FooterMenuApi(FooterMenuPublicService service) {
    this.service = service;
  }

  @GetMapping(value = "/v3/{brand}/footer-menu")
  public ResponseEntity findByBrand(@PathVariable("brand") String brand) {
    List<FooterMenuV3Dto> list = service.find(brand);

    return CollectionUtils.isEmpty(list)
        ? new ResponseEntity<>(HttpStatus.NO_CONTENT)
        : new ResponseEntity<>(list, HttpStatus.OK);
  }

  @GetMapping(value = "/v2/{brand}/footer-menu/{deviceType}")
  public List<FooterMenuV2Dto> findByBrand(
      @PathVariable("brand") String brand, @PathVariable("deviceType") String deviceType) {
    return service.find(brand, deviceType);
  }
}
