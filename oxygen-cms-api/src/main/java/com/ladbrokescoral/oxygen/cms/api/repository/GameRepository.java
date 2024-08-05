package com.ladbrokescoral.oxygen.cms.api.repository;

import com.ladbrokescoral.oxygen.cms.api.entity.Game;
import java.time.Instant;
import java.util.List;

public interface GameRepository extends CustomMongoRepository<Game> {

  List<Game> findByDisplayFromIsBeforeAndDisplayToIsAfterAndBrandIsAndEnabledIsTrueAndIdNot(
      Instant displayFrom, Instant displayTo, String brand, String gameId);

  List<Game> findByDisplayFromIsBeforeAndDisplayToIsAfterAndBrandIsAndEnabledIsTrue(
      Instant displayFrom, Instant displayTo, String brand);

  List<Game> findByDisplayToIsBeforeAndBrandIsAndEnabledIsTrueOrderByDisplayToDesc(
      Instant displayTo, String brand);

  default List<Game> findLastBeforeActive(String brand) {
    return findByDisplayToIsBeforeAndBrandIsAndEnabledIsTrueOrderByDisplayToDesc(
        Instant.now(), brand);
  }

  List<Game> findBySeasonId(String seasonId);

  List<Game> findByDisplayFromIsGreaterThanEqualAndBrandIsAndEnabledIsTrue(
      Instant displayFrom, String brand);
}
