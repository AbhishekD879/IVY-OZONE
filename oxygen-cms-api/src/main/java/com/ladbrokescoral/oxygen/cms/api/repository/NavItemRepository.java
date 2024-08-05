package com.ladbrokescoral.oxygen.cms.api.repository;

import com.ladbrokescoral.oxygen.cms.api.entity.NavItem;
import java.util.List;
import java.util.Set;
import org.springframework.data.domain.Sort;

public interface NavItemRepository extends CustomMongoRepository<NavItem> {

  List<NavItem> findAllNavItemByNavigationGroupId(String id, Sort sort);

  List<NavItem> findAllNavItemByBrand(String brand);

  void deleteByNavigationGroupId(String navigationGroupId);

  List<NavItem> findAllNavItemByLeaderboardId(String id);

  List<NavItem> findAllByBrandAndLeaderboardIdNotNull(String brand);

  List<NavItem> findAllByBrandAndNavTypeEqualsIgnoreCaseAndNavigationGroupIdIn(
      String brand, String navType, Set<String> navGroupIds);

  List<NavItem> findAllNavItemByNavTypeEqualsIgnoreCaseAndNavigationGroupId(
      String navType, String navigationId);
}
