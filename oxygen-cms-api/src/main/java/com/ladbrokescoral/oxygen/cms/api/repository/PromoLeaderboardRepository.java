package com.ladbrokescoral.oxygen.cms.api.repository;

import com.ladbrokescoral.oxygen.cms.api.entity.PromoLeaderboardConfig;
import java.util.List;
import java.util.Optional;

public interface PromoLeaderboardRepository extends CustomMongoRepository<PromoLeaderboardConfig> {
  Optional<PromoLeaderboardConfig> findByBrandAndId(String brand, String leaderboardId);

  List<PromoLeaderboardConfig> findAllByIdIn(List<String> lbrIds);
}
