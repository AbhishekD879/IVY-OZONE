package com.ladbrokescoral.oxygen.cms.api.repository;

import com.ladbrokescoral.oxygen.cms.api.entity.Season;
import java.time.Instant;
import java.util.List;

public interface SeasonRepository extends CustomMongoRepository<Season> {

  List<Season> findByBrandAndDisplayToIsGreaterThanEqualAndDisplayFromIsLessThan(
      String brand, Instant fromDate, Instant toDate);

  List<Season> findByBrandAndDisplayFromIsLessThanEqualAndDisplayToGreaterThanEqual(
      String brand, Instant toDate, Instant fromDate);

  List<Season> findByBrandAndDisplayFromIsGreaterThanEqual(String brand, Instant toDate);
}
