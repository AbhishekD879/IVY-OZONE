package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import com.ladbrokescoral.oxygen.cms.api.dto.SportPage;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.SportPagePublicService;
import java.util.List;
import java.util.Optional;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequiredArgsConstructor
public class SportPageApi implements Public {
  private final SportPagePublicService sportPagePublicService;

  @GetMapping(value = {"{brand}/sports-pages", "{brand}/sports-pages/{lastRunDate}"})
  public List<SportPage> findAllPagesByBrand(
      @PathVariable("brand") String brand, @PathVariable Optional<Long> lastRunDate) {
    return sportPagePublicService.findAllPagesByBrand(
        brand, lastRunDate.isPresent() ? lastRunDate.get() : 0);
  }
}
