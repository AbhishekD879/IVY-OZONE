package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import com.ladbrokescoral.oxygen.cms.api.service.public_api.MaintenancePagePublicService;
import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.util.CollectionUtils;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class MaintenancePageApi implements Public {

  private final MaintenancePagePublicService service;

  @Autowired
  public MaintenancePageApi(MaintenancePagePublicService service) {
    this.service = service;
  }

  @GetMapping(value = "{brand}/maintenance-page/{deviceType}")
  public ResponseEntity findByBrand(
      @PathVariable("brand") String brand, @PathVariable("deviceType") String deviceType) {

    List list = service.findMaintenanePages(brand, deviceType);

    return CollectionUtils.isEmpty(list)
        ? new ResponseEntity<>(HttpStatus.NO_CONTENT)
        : new ResponseEntity<>(list, HttpStatus.OK);
  }
}
