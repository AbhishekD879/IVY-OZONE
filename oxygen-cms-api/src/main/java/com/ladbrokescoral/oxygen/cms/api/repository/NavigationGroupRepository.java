package com.ladbrokescoral.oxygen.cms.api.repository;

import com.ladbrokescoral.oxygen.cms.api.entity.NavigationGroup;
import java.util.List;

public interface NavigationGroupRepository extends CustomMongoRepository<NavigationGroup> {

  List<NavigationGroup> findAllNavigationGroupByBrandAndStatusIsTrue(String brand);
}
