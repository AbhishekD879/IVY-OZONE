package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import com.ladbrokescoral.oxygen.cms.api.service.public_api.WidgetPublicService;
import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.util.CollectionUtils;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class WidgetApi implements Public {

  private final WidgetPublicService service;

  @Autowired
  public WidgetApi(WidgetPublicService service) {
    this.service = service;
  }

  @GetMapping(value = "{brand}/widgets")
  public ResponseEntity findByBrand(@PathVariable("brand") String brand) {
    List list = service.findByBrand(brand);
    return CollectionUtils.isEmpty(list)
        ? new ResponseEntity<>(HttpStatus.NO_CONTENT)
        : new ResponseEntity<>(list, HttpStatus.OK);
  }
}
