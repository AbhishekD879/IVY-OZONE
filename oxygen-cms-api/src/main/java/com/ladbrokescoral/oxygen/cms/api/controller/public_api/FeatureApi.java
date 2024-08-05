package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import com.ladbrokescoral.oxygen.cms.api.dto.FeatureContainerDto;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.FeaturePublicService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.util.CollectionUtils;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class FeatureApi implements Public {

  private final FeaturePublicService featureService;

  @Autowired
  public FeatureApi(FeaturePublicService featureService) {
    this.featureService = featureService;
  }

  @GetMapping(value = "{brand}/features")
  public ResponseEntity findByBrand(@PathVariable("brand") String brand) {
    FeatureContainerDto container = featureService.findContainerByBrand(brand);

    return CollectionUtils.isEmpty(container.getFeatures())
        ? new ResponseEntity<>(HttpStatus.NO_CONTENT)
        : new ResponseEntity<>(container, HttpStatus.OK);
  }
}
