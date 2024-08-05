package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.entity.LeagueLink;
import com.ladbrokescoral.oxygen.cms.api.repository.impl.LeagueLinkRepository;
import java.util.List;
import org.springframework.stereotype.Service;

@Service
public class LeagueLinkService extends AbstractService<LeagueLink> {

  private final LeagueLinkRepository leagueLinkRepository;

  public LeagueLinkService(LeagueLinkRepository leagueLinkRepository) {
    super(leagueLinkRepository);
    this.leagueLinkRepository = leagueLinkRepository;
  }

  public List<LeagueLink> getEnabledLeagueLinksByCouponId(String brand, int couponId) {
    return leagueLinkRepository.findByCouponIdsContainsAndEnabledTrueAndBrandEquals(
        couponId, brand);
  }
}
