package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import com.ladbrokescoral.oxygen.cms.api.dto.InitSignpostingDto;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.InitSignpostingPublicService;
import java.util.List;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.util.CollectionUtils;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class InitSignpostingApi implements Public {

  private InitSignpostingPublicService service;

  public InitSignpostingApi(InitSignpostingPublicService service) {
    this.service = service;
  }

  @GetMapping(value = "/{brand}/init-signposting")
  public ResponseEntity findByBrand(@PathVariable("brand") String brand) {
    List<InitSignpostingDto> list = service.find(brand);

    return CollectionUtils.isEmpty(list)
        ? new ResponseEntity<>(HttpStatus.NO_CONTENT)
        : new ResponseEntity<>(list, HttpStatus.OK);
  }
}
