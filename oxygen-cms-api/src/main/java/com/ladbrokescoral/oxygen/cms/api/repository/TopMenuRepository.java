package com.ladbrokescoral.oxygen.cms.api.repository;

import com.ladbrokescoral.oxygen.cms.api.entity.TopMenu;
import java.util.List;

public interface TopMenuRepository extends CustomMongoRepository<TopMenu> {

  List<TopMenu> findAllByBrandAndDisabledOrderBySortOrderAsc(String brand, Boolean disabled);
}
