package com.ladbrokescoral.oxygen.cms.api.repository;

import com.ladbrokescoral.oxygen.cms.api.entity.NavigationPoint;
import java.util.List;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.mongodb.repository.Query;

public interface NavigationPointRepository extends CustomSegmentRepository<NavigationPoint> {
  @Query("{'brand' : ?0, 'enabled': true}")
  List<NavigationPoint> findAllActiveRecordsByBrand(String brand, PageRequest pageRequest);
}
