package com.ladbrokescoral.oxygen.cms.api.dto;

import com.google.common.base.CaseFormat;
import com.ladbrokescoral.oxygen.cms.api.controller.dto.Filters;
import com.ladbrokescoral.oxygen.cms.api.dto.SportTabConfigDto.SportTabConfigDtoBuilder;
import com.ladbrokescoral.oxygen.cms.api.entity.SportTab;
import com.ladbrokescoral.oxygen.cms.api.entity.SportTabMarket;
import com.ladbrokescoral.oxygen.cms.api.entity.TrendingTab;
import com.ladbrokescoral.oxygen.cms.api.service.sporttab.SportTabHelper;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;
import lombok.Data;
import org.modelmapper.ModelMapper;
import org.springframework.util.CollectionUtils;

// FIXME: need rework. no need for isolated builder
@Data
class SportTabConfigBuilder {

  private static final String ID_PREFIX = "tab-";
  private List<SportTabConfigDto> tabs = new ArrayList<>();
  private final String baseTargetUri;

  public void addTab(SportTab tab) {
    String tabName = tab.getName();
    SportTabHelper.sortTrendingTabs(tab);
    SportTabConfigDtoBuilder sportTabConfigBuilder =
        SportTabConfigDto.builder()
            .id(ID_PREFIX + tabName)
            .name(tabName)
            .label(tab.getDisplayName())
            .url(String.format("/%s/%s", baseTargetUri, tabName))
            .marketsNames(getMarkets(tab.getMarketsNames()))
            .sortOrder(tab.getSortOrder())
            .interstitialBanners(tab.getInterstitialBanners())
            .hidden(tab.isHidden())
            .trendingTabs(getTrendingTabs(tab.getTrendingTabs()))
            .showNewFlag(tab.getShowNewFlag());

    Optional.ofNullable(tab.getFilters())
        .map(Filters::toSimplifiedFilters)
        .ifPresent(sportTabConfigBuilder::filters);

    tabs.add(sportTabConfigBuilder.build());
  }

  private List<SportTabMarketConfigDto> getMarkets(List<SportTabMarket> sportTabMarkets) {
    if (sportTabMarkets == null || sportTabMarkets.isEmpty()) return Collections.emptyList();
    return sportTabMarkets.stream()
        .map(e -> new ModelMapper().map(e, SportTabMarketConfigDto.class))
        .collect(Collectors.toList());
  }

  private List<TrendingTabConfigDto> getTrendingTabs(List<TrendingTab> trendingTabs) {
    if (CollectionUtils.isEmpty(trendingTabs)) return Collections.emptyList();
    return trendingTabs.stream()
        .map(tab -> new ModelMapper().map(tab, TrendingTabConfigDto.class))
        .collect(Collectors.toList());
  }

  public void addSubTab(String tabName) {
    if (tabs.isEmpty()) {
      throw new IllegalArgumentException(
          "Unable to add subTab %s into %s config due to tabs absence");
    }
    SportTabConfigDto lastTab = tabs.get(tabs.size() - 1);
    lastTab.addSubTab(
        SportTabConfigDto.builder()
            .id(ID_PREFIX + tabName)
            .name(tabName)
            .label(CaseFormat.LOWER_CAMEL.to(CaseFormat.UPPER_CAMEL, tabName))
            .url(String.format("%s/%s", lastTab.getUrl(), tabName))
            .hidden(false)
            .build());
  }
}
