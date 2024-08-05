package com.ladbrokescoral.oxygen.cms.api.service.sporttab;

import com.ladbrokescoral.oxygen.cms.api.entity.SportCategory;
import com.ladbrokescoral.oxygen.cms.api.entity.SportTab;
import java.util.List;
import java.util.stream.Collectors;

public abstract class SportTabsTemplate {
  public abstract boolean isValidForSport(SportCategory sportCategory);

  protected abstract List<SportTab> getTabsBySport(String ssCategoryCode);

  public List<SportTab> buildTabs(SportCategory sportCategory) {
    return getTabsBySport(sportCategory.getSsCategoryCode()).stream()
        .map(this::copyTab)
        .map(tab -> populateTab(tab, sportCategory))
        .collect(Collectors.toList());
  }

  private SportTab copyTab(SportTab sportTab) {
    return createTab(
        sportTab.getName(),
        sportTab.getDisplayName(),
        sportTab.getSortOrder(),
        sportTab.isCheckEvents(),
        sportTab.isEnabled());
  }

  public static SportTab createTab(
      String name, String displayName, Double sortOrder, boolean checkEvents, boolean enabled) {
    return SportTab.builder()
        .name(name)
        .displayName(displayName)
        .sortOrder(sortOrder)
        .enabled(enabled)
        .checkEvents(checkEvents)
        .build();
  }

  private SportTab populateTab(SportTab sportTab, SportCategory sportCategory) {
    sportTab.setBrand(sportCategory.getBrand());
    sportTab.setSportId(sportCategory.getCategoryId());
    return sportTab;
  }
}
