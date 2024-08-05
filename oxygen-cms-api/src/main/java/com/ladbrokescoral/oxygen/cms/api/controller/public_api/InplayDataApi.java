package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import com.ladbrokescoral.oxygen.cms.api.dto.InplayDataDto;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.InplayDataPublicService;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequiredArgsConstructor
public class InplayDataApi implements Public {

  private final InplayDataPublicService service;

  @GetMapping(value = "{brand}/inplay-data")
  public InplayDataDto getInplayData(@PathVariable("brand") String brand) {
    return service.getInplayData(brand);
  }
}
