package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import com.ladbrokescoral.oxygen.cms.api.dto.FiveASideFormationDto;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.FiveASideFormationsPublicService;
import java.util.List;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequiredArgsConstructor
public class FiveASideFormationsApi implements Public {
  private final FiveASideFormationsPublicService service;

  @GetMapping("{brand}/five-a-side-formations")
  public List<FiveASideFormationDto> findByBrand(@PathVariable("brand") String brand) {
    return service.findAll(brand);
  }
}
