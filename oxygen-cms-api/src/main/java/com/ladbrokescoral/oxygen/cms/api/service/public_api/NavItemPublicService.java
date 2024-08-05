package com.ladbrokescoral.oxygen.cms.api.service.public_api;

import com.ladbrokescoral.oxygen.cms.api.dto.NavItemPublicDto;
import com.ladbrokescoral.oxygen.cms.api.dto.NavigationGroupPublicDto;
import com.ladbrokescoral.oxygen.cms.api.entity.*;
import com.ladbrokescoral.oxygen.cms.api.service.NavItemService;
import com.ladbrokescoral.oxygen.cms.api.service.NavigationGroupService;
import java.util.*;
import java.util.stream.Collectors;
import org.modelmapper.ModelMapper;
import org.modelmapper.TypeToken;
import org.springframework.stereotype.Service;

@Service
public class NavItemPublicService {

  private final NavItemService navItemService;

  private final NavigationGroupService navigationGroupService;

  private final ModelMapper modelMapper;

  public NavItemPublicService(
      NavItemService navItemService,
      NavigationGroupService navigationGroupService,
      ModelMapper modelMapper) {
    this.navItemService = navItemService;
    this.navigationGroupService = navigationGroupService;
    this.modelMapper = modelMapper;
  }

  public List<NavigationGroupPublicDto> getNavigationGroupByBrand(String brand) {

    List<NavItem> allNavItem = navItemService.findAllNavItem(brand);

    List<NavigationGroup> activeNavigationGroups =
        navigationGroupService.findAllActiveNavigationGroupByBrand(brand);

    Set<String> navigationGroupIds =
        activeNavigationGroups.stream().map(AbstractEntity::getId).collect(Collectors.toSet());

    Map<String, List<NavItem>> allSortedNavItem =
        sortedNavigationGroupNavItem(allNavItem, navigationGroupIds);

    return activeNavigationGroups.stream()
        .map(navGroup -> modelMapper.map(navGroup, NavigationGroupPublicDto.class))
        .map(
            (NavigationGroupPublicDto navG) -> {
              List<NavItem> navItemList = allSortedNavItem.get(navG.getId());
              if (Objects.nonNull(navItemList)) {
                navG.setNavItems(
                    modelMapper.map(
                        navItemService.getNavItemWithActiveLbr(navItemList),
                        new TypeToken<List<NavItemPublicDto>>() {}.getType()));
              }
              return navG;
            })
        .collect(Collectors.toList());
  }

  private Map<String, List<NavItem>> sortedNavigationGroupNavItem(
      List<NavItem> allNavItem, Set<String> navigationGroupIds) {
    Map<String, List<NavItem>> navItems =
        allNavItem.stream()
            .filter(navG -> navigationGroupIds.contains(navG.getNavigationGroupId()))
            .collect(Collectors.groupingBy(NavItem::getNavigationGroupId));
    navItems.forEach(
        (String k, List<NavItem> v) -> {
          v.sort(Comparator.comparing(SortableEntity::getSortOrder));
          navItems.put(k, v);
        });
    return navItems;
  }
}
