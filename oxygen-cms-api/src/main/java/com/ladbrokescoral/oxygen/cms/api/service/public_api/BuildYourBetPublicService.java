package com.ladbrokescoral.oxygen.cms.api.service.public_api;

import com.ladbrokescoral.oxygen.cms.api.service.YourCallLeagueService;
import java.util.List;
import java.util.Set;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.cache.annotation.CachePut;
import org.springframework.cache.annotation.Cacheable;
import org.springframework.stereotype.Component;

@Slf4j
@Component
@RequiredArgsConstructor
public class BuildYourBetPublicService {

  private final BanachService banachService;
  private final YourCallLeagueService yourCallLeagueService;

  @Cacheable("buildyourbet-leagues-available")
  public boolean isAtLeastOneBanachEventAvailable(String brand) {
    return calculateAtLeastOneBanachEventAvailable(brand);
  }

  @CachePut("buildyourbet-leagues-available")
  public boolean calculateAtLeastOneBanachEventAvailable(String brand) {
    Set<Long> disabledLeaguesIds = yourCallLeagueService.findDisabledBuildYourBetLeaguesIds(brand);
    List<Long> banachLeaguesIds = banachService.getBanachLeaguesIds(brand);
    banachLeaguesIds.removeAll(disabledLeaguesIds);
    log.debug(
        "[{}] Disabled leaguesIds: {}. Banach leagues: {}",
        brand,
        disabledLeaguesIds,
        banachLeaguesIds);
    return !banachLeaguesIds.isEmpty();
  }
}
