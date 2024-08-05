package com.ladbrokescoral.oxygen.cms.api.dto;

import com.ladbrokescoral.oxygen.cms.api.entity.SportCategory;
import java.util.LinkedHashMap;
import java.util.Map;
import lombok.Data;

// FIXME: need rework. no need for isolated builder
@Data
public class TabFiltersBuilder {

  private final SportCategory sportCategory;
  private Map<String, SSTabRequestFilters> tabRequestsFilters;

  public void build() {
    this.tabRequestsFilters = new LinkedHashMap<>();
    this.tabRequestsFilters.put("live", new SSTabRequestFilters());
    this.tabRequestsFilters.put(
        "coupons", new SSTabRequestFilters().setActive(true).setDate("today"));

    boolean isFootball = "FOOTBALL".equalsIgnoreCase(sportCategory.getSsCategoryCode());
    Boolean templateMarketNameOnlyIntersects = isFootball ? Boolean.TRUE : null;

    this.tabRequestsFilters.put(
        "today",
        new SSTabRequestFilters()
            .setTemplateMarketNameOnlyIntersects(templateMarketNameOnlyIntersects)
            .setNotStarted(true));
    this.tabRequestsFilters.put(
        "tomorrow",
        new SSTabRequestFilters()
            .setTemplateMarketNameOnlyIntersects(templateMarketNameOnlyIntersects));
    this.tabRequestsFilters.put(
        "future",
        new SSTabRequestFilters()
            .setTemplateMarketNameOnlyIntersects(templateMarketNameOnlyIntersects));

    this.tabRequestsFilters.put(
        "outrights", new SSTabRequestFilters().setActive(true).setMarketsCount(false));

    if (isFootball) {
      fillUpFootballTabFilters();
    }
  }

  private void fillUpFootballTabFilters() {
    this.tabRequestsFilters.put("upcoming", new SSTabRequestFilters().setNotStarted(true));
    this.tabRequestsFilters.put(
        "specials",
        new SSTabRequestFilters().setMarketsCount(false).setDrilldownTagNames("MKTFLAG_SP"));
    this.tabRequestsFilters.put("jackpot", new SSTabRequestFilters());
    this.tabRequestsFilters.put("results", new SSTabRequestFilters());
  }
}
