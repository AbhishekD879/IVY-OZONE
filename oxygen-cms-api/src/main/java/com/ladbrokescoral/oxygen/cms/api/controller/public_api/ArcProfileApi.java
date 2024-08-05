package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import com.ladbrokescoral.oxygen.cms.api.dto.ArcProfileDto;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.ArcProfilePublicService;
import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.util.CollectionUtils;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class ArcProfileApi implements Public {
  private ArcProfilePublicService service;

  @Autowired
  public ArcProfileApi(ArcProfilePublicService service) {
    this.service = service;
  }

  @GetMapping(value = "{brand}/arc-profile")
  public ResponseEntity<List<ArcProfileDto>> findByBrand(@PathVariable("brand") String brand) {
    List<ArcProfileDto> list = service.findByBrand(brand);
    return CollectionUtils.isEmpty(list)
        ? new ResponseEntity<>(HttpStatus.NOT_FOUND)
        : new ResponseEntity<>(list, HttpStatus.OK);
  }

  @GetMapping("arc-profile/{id}")
  public ArcProfileDto findById(@PathVariable("id") String id) {
    return service.findById(id);
  }

  @GetMapping("{brand}/arc-profile/{modelAndRiskLevel}/{reasonCode}")
  public ResponseEntity<ArcProfileDto> read(
      @PathVariable String brand,
      @PathVariable Integer modelAndRiskLevel,
      @PathVariable Integer reasonCode) {
    ArcProfileDto arcProfileDto =
        service.findArcProfileByBrandAndModelRiskLevelAndReasonCode(
            brand, modelAndRiskLevel, reasonCode);
    return null == arcProfileDto
        ? new ResponseEntity<>(HttpStatus.NOT_FOUND)
        : new ResponseEntity<>(arcProfileDto, HttpStatus.OK);
  }
}
