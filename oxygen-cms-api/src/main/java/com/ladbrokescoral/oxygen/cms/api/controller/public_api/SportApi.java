package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import com.ladbrokescoral.oxygen.cms.api.dto.SportDto;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.SportPublicService;
import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.util.CollectionUtils;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class SportApi implements Public {

  private final SportPublicService service;

  @Autowired
  public SportApi(SportPublicService service) {
    this.service = service;
  }

  @GetMapping(value = "{brand}/sports")
  public ResponseEntity findByBrand(@PathVariable("brand") String brand) {
    List<SportDto> list = service.find(brand);
    return CollectionUtils.isEmpty(list)
        ? new ResponseEntity<>(HttpStatus.NO_CONTENT)
        : new ResponseEntity<>(list, HttpStatus.OK);
  }
}
