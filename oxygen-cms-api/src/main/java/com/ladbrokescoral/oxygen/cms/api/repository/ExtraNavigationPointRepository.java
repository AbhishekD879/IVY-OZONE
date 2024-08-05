package com.ladbrokescoral.oxygen.cms.api.repository;

import com.ladbrokescoral.oxygen.cms.api.entity.ExtraNavigationPoint;
import java.util.List;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.mongodb.repository.Query;

public interface ExtraNavigationPointRepository
    extends CustomMongoRepository<ExtraNavigationPoint> {

  @Query("{'brand' : ?0, 'enabled': true}")
  List<ExtraNavigationPoint> findAllActiveRecordsByBrand(String brand, PageRequest pageRequest);
}
