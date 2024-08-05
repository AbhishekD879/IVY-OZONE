package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import com.ladbrokescoral.oxygen.cms.api.dto.ExternalLinkDto;
import com.ladbrokescoral.oxygen.cms.api.mapping.ExternalLinkMapper;
import com.ladbrokescoral.oxygen.cms.api.service.ExternalLinkService;
import java.util.List;
import java.util.stream.Collectors;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class ExternalLinkApi implements Public {

  private final ExternalLinkService service;

  public ExternalLinkApi(ExternalLinkService service) {
    this.service = service;
  }

  @GetMapping("{brand}/external-link")
  public List<ExternalLinkDto> findByBrand(@PathVariable("brand") String brand) {
    return service.findByBrand(brand).stream()
        .map(ExternalLinkMapper.INSTANCE::toDto)
        .collect(Collectors.toList());
  }
}
