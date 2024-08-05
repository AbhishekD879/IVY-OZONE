package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import com.ladbrokescoral.oxygen.cms.api.entity.Overlay;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.OverlayPublicService;
import java.util.Optional;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class OverlayApi implements Public {
  private final OverlayPublicService service;

  @Autowired
  public OverlayApi(OverlayPublicService service) {
    this.service = service;
  }

  /**
   * List All Overlay based on Brand
   *
   * @param brand - Brand
   */
  @GetMapping(value = "{brand}/overlay")
  public ResponseEntity<Overlay> readByBrand(@PathVariable String brand) {
    Optional<Overlay> optionalOverlay = service.findOneByBrand(brand);
    if (optionalOverlay.isPresent()) {
      Overlay overlay = optionalOverlay.get();
      return new ResponseEntity<>(overlay, HttpStatus.OK);
    }
    return new ResponseEntity<>(HttpStatus.NO_CONTENT);
  }
}
