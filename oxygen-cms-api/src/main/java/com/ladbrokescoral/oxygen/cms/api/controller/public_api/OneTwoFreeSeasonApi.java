package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import com.ladbrokescoral.oxygen.cms.api.dto.SeasonCacheDto;
import com.ladbrokescoral.oxygen.cms.api.dto.SeasonDto;
import com.ladbrokescoral.oxygen.cms.api.dto.SeasonGamificationDto;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.SeasonPublicService;
import java.util.List;
import java.util.Optional;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequiredArgsConstructor
public class OneTwoFreeSeasonApi implements Public {

  private final SeasonPublicService seasonPublicService;

  @GetMapping("{brand}/one-two-free/season")
  public List<SeasonDto> findAllSeasonByBrand(@PathVariable String brand) {
    return seasonPublicService.findAllByBrand(brand);
  }

  @GetMapping("{brand}/one-two-free/current-future-seasons")
  public List<SeasonGamificationDto> getCurrentFutureSeasons(@PathVariable String brand) {
    return seasonPublicService.getCurrentFutureSeasons(brand);
  }

  @GetMapping("{brand}/one-two-free/active-season")
  public Optional<SeasonCacheDto> getActiveSeason(@PathVariable String brand) {
    return seasonPublicService.getActiveSeason(brand);
  }

  @GetMapping("{brand}/one-two-free/current-future-seasons-v2")
  public List<SeasonCacheDto> findAllCurrentAndFutureSeasons(@PathVariable String brand) {
    return seasonPublicService.getCurrentFutureSeasonDetails(brand);
  }
}
