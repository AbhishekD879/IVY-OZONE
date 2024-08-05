package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import com.ladbrokescoral.oxygen.cms.api.dto.FooterLogoDto;
import com.ladbrokescoral.oxygen.cms.api.dto.FooterLogoNativeDto;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.FooterLogoPublicService;
import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.util.CollectionUtils;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class FooterLogoApi implements Public {

  private final FooterLogoPublicService service;

  @Autowired
  public FooterLogoApi(FooterLogoPublicService service) {
    this.service = service;
  }

  @GetMapping(value = "{brand}/footer-logos-native")
  public ResponseEntity findByBrandNative(@PathVariable("brand") String brand) {
    List<FooterLogoNativeDto> list = service.findNative(brand);
    return CollectionUtils.isEmpty(list)
        ? new ResponseEntity<>(HttpStatus.NO_CONTENT)
        : new ResponseEntity<>(list, HttpStatus.OK);
  }

  @GetMapping(value = "{brand}/footer-logos")
  public ResponseEntity findByBrand(@PathVariable("brand") String brand) {
    List<FooterLogoDto> list = service.find(brand);
    return CollectionUtils.isEmpty(list)
        ? new ResponseEntity<>(HttpStatus.NO_CONTENT)
        : new ResponseEntity<>(list, HttpStatus.OK);
  }
}
