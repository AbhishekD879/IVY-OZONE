package com.ladbrokescoral.oxygen.cms.api.repository;

import com.ladbrokescoral.oxygen.cms.api.entity.Gamification;
import java.util.List;
import java.util.Optional;

public interface GamificationRepository extends CustomMongoRepository<Gamification> {
  Optional<Gamification> findBySeasonId(String seasonId);

  List<Optional<Gamification>> findBySeasonIdIn(List<String> seasonIds);
}
