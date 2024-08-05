package com.ladbrokescoral.oxygen.cms.api.repository;

import com.ladbrokescoral.oxygen.cms.api.entity.Dashboard;
import java.time.Instant;
import java.util.List;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.mongodb.repository.Query;

public interface DashboardRepository extends CustomMongoRepository<Dashboard> {
  @Override
  Page<Dashboard> findAll(Pageable pageable);

  void removeDashboardsByCreatedAtBefore(Instant date);

  @Query("{" + "'createdAt': {'$gte': ?0, '$lte': ?1}" + "}")
  List<Dashboard> findDashboardsByCreatedAt(Instant start, Instant end);
}
