package com.ladbrokescoral.oxygen.cms.api.repository;

import com.ladbrokescoral.oxygen.cms.api.entity.Contest;
import java.time.Instant;
import java.util.List;

/** Contests Repository */
public interface ContestRepository extends CustomMongoRepository<Contest> {

  List<Contest> findAllByBrandOrderBySortOrderAsc(String brand);

  public List<Contest> findByBrandAndEventAndDisplayTrue(String brand, String event);

  public List<Contest> findByStartDateBetween(Instant today, Instant tomorrow);

  public List<Contest> findByBrandAndStartDateGreaterThan(String brand, Instant fromDate);

  public List<Contest> findByBrandAndEventInAndDisplayTrue(String brand, List<String> events);

  public List<Contest> findByBrandAndDisplayTrue(String brand);
}
