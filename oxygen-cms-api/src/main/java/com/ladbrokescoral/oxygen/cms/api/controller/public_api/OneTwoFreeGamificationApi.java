package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import com.ladbrokescoral.oxygen.cms.api.dto.GamificationDetailsPublicDto;
import com.ladbrokescoral.oxygen.cms.api.service.GamificationPublicService;
import java.util.List;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequiredArgsConstructor
public class OneTwoFreeGamificationApi implements Public {
  private final GamificationPublicService gamificationPublicService;

  @GetMapping("{brand}/one-two-free/gamification")
  public List<GamificationDetailsPublicDto> findGamificationByBrand(@PathVariable String brand) {
    return gamificationPublicService.findGamificationByBrand(brand);
  }
}
