package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import com.ladbrokescoral.oxygen.cms.api.dto.OnBoardingGuideDto;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.OnBoardingGuidePublicService;
import java.util.List;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequiredArgsConstructor
public class OnBoardingGuidesApi implements Public {

  private final OnBoardingGuidePublicService service;

  @GetMapping("{brand}/on-boarding-guide")
  public List<OnBoardingGuideDto> findOnBoardingGuidesByBrand(@PathVariable String brand) {
    return service.getOnBoardingGuides(brand);
  }
}
