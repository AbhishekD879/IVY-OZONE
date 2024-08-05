package com.ladbrokescoral.oxygen.cms.api.repository.impl;

import com.ladbrokescoral.oxygen.cms.api.entity.LeagueLink;
import com.ladbrokescoral.oxygen.cms.api.repository.CustomMongoRepository;
import java.util.List;

public interface LeagueLinkRepository extends CustomMongoRepository<LeagueLink> {
  List<LeagueLink> findByCouponIdsContainsAndEnabledTrueAndBrandEquals(int couponId, String brand);
}
