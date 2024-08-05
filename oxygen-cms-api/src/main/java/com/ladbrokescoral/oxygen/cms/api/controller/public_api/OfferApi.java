package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import com.ladbrokescoral.oxygen.cms.api.dto.OfferModuleDto;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.OfferPublicService;
import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.util.CollectionUtils;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class OfferApi implements Public {

  private final OfferPublicService service;

  @Autowired
  public OfferApi(OfferPublicService service) {
    this.service = service;
  }

  @GetMapping(value = "/v2/{brand}/offers/{deviceType}")
  public ResponseEntity findByBrand(
      @PathVariable("brand") String brand, @PathVariable("deviceType") String deviceType) {

    if (!deviceType.equals("tablet") && !deviceType.equals("desktop")) {
      return new ResponseEntity<>(HttpStatus.NO_CONTENT);
    }

    List<OfferModuleDto> result = service.findByBrand(brand, deviceType);
    return CollectionUtils.isEmpty(result)
        ? new ResponseEntity<>(HttpStatus.NO_CONTENT)
        : new ResponseEntity<>(result, HttpStatus.OK);
  }
}
