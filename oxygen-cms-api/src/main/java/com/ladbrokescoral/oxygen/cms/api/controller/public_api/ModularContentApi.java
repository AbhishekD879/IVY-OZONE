package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import com.ladbrokescoral.oxygen.cms.api.dto.BaseModularContentDto;
import com.ladbrokescoral.oxygen.cms.api.entity.HomeModule;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.ModularContentPublicService;
import java.util.List;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.util.CollectionUtils;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class ModularContentApi implements Public {

  private final ModularContentPublicService service;

  public ModularContentApi(ModularContentPublicService service) {
    this.service = service;
  }

  @GetMapping(value = "{brand}/modular-content")
  public ResponseEntity findByBrand(@PathVariable("brand") String brand) {
    List<BaseModularContentDto> list = service.findUniversalByBrand(brand);
    return CollectionUtils.isEmpty(list)
        ? new ResponseEntity<>(HttpStatus.NO_CONTENT)
        : new ResponseEntity<>(list, HttpStatus.OK);
  }

  @GetMapping(value = "{brand}/personalised-modular-content")
  public ResponseEntity findPersonalisedByBrand(@PathVariable("brand") String brand) {
    List<HomeModule> list = service.findPersonalised(brand);
    return CollectionUtils.isEmpty(list)
        ? new ResponseEntity<>(HttpStatus.NO_CONTENT)
        : new ResponseEntity<>(list, HttpStatus.OK);
  }
}
