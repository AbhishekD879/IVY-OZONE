package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import com.ladbrokescoral.oxygen.cms.api.dto.BannerDto;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.BannerPublicService;
import java.util.List;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.util.CollectionUtils;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class BannerApi implements Public {

  private final BannerPublicService service;

  public BannerApi(BannerPublicService service) {
    this.service = service;
  }

  @GetMapping("v2/{brand}/banners/{category}")
  public ResponseEntity findByBrandAndCategory(
      @PathVariable("brand") String brand, @PathVariable("category") String category) {
    List<BannerDto> list = service.find(brand, category);
    return CollectionUtils.isEmpty(list)
        ? new ResponseEntity<>(HttpStatus.NO_CONTENT)
        : new ResponseEntity<>(list, HttpStatus.OK);
  }
}
