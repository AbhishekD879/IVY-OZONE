package com.ladbrokescoral.oxygen.cms.api.repository;

import com.ladbrokescoral.oxygen.cms.api.entity.TopGame;
import java.util.List;

public interface TopGameRepository extends CustomMongoRepository<TopGame> {
  List<TopGame> findAllByBrandOrderBySortOrderAsc(String brand);
}
