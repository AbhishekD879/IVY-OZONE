package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import com.ladbrokescoral.oxygen.cms.api.entity.Football3DBanner;
import com.ladbrokescoral.oxygen.cms.api.mapping.Football3DBannerMapper;
import com.ladbrokescoral.oxygen.cms.api.service.Football3DBannerService;
import java.util.List;
import java.util.stream.Collectors;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.util.CollectionUtils;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class Footbal3DBannerApi implements Public {

  private final Football3DBannerService service;

  @Autowired
  public Footbal3DBannerApi(Football3DBannerService service) {
    this.service = service;
  }

  @GetMapping(value = "{brand}/3d-football-banners")
  public ResponseEntity findByBrand(@PathVariable("brand") String brand) {
    List<Football3DBanner> football3DBannerCollection = service.findAllByBrandAndDisabled(brand);
    List list =
        football3DBannerCollection.stream()
            .map(Football3DBannerMapper.INSTANCE::toDto)
            .collect(Collectors.toList());
    return CollectionUtils.isEmpty(list)
        ? new ResponseEntity<>(HttpStatus.NO_CONTENT)
        : new ResponseEntity<>(list, HttpStatus.OK);
  }
}
