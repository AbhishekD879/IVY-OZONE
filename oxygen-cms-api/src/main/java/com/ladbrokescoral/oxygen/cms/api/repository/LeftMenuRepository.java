package com.ladbrokescoral.oxygen.cms.api.repository;

import com.ladbrokescoral.oxygen.cms.api.entity.LeftMenu;
import java.util.List;

public interface LeftMenuRepository extends CustomMongoRepository<LeftMenu> {
  List<LeftMenu> findAllByBrandOrderBySortOrderAsc(String brand);
}
