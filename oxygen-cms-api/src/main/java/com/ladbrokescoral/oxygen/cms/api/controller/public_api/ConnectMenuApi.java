package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import com.ladbrokescoral.oxygen.cms.api.dto.ConnectMenuDto;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.ConnectMenuPublicService;
import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.util.CollectionUtils;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class ConnectMenuApi implements Public {

  private final ConnectMenuPublicService service;

  @Autowired
  public ConnectMenuApi(ConnectMenuPublicService service) {
    this.service = service;
  }

  @GetMapping(value = {"{brand}/connect-menu"})
  public ResponseEntity findByBrand(@PathVariable("brand") String brand) {
    List<ConnectMenuDto> list = service.findByBrand(brand);
    return CollectionUtils.isEmpty(list)
        ? new ResponseEntity<>(HttpStatus.NO_CONTENT)
        : new ResponseEntity<>(list, HttpStatus.OK);
  }
}
