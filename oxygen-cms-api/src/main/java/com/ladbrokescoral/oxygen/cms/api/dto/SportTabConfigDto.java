package com.ladbrokescoral.oxygen.cms.api.dto;

import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonInclude.Include;
import com.ladbrokescoral.oxygen.cms.api.controller.dto.PublicApiFilters;
import com.ladbrokescoral.oxygen.cms.api.entity.InitialBanner;
import java.util.ArrayList;
import java.util.List;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.EqualsAndHashCode;
import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
@Builder
@AllArgsConstructor
@EqualsAndHashCode
@JsonInclude(Include.NON_EMPTY)
public class SportTabConfigDto {

  private String id;
  private String name;
  private String label;
  private String url;
  private boolean hidden;
  private Double sortOrder;
  private List<SportTabConfigDto> subTabs;
  private PublicApiFilters filters;
  private List<SportTabMarketConfigDto> marketsNames = new ArrayList<>();
  private InitialBanner interstitialBanners;

  private List<TrendingTabConfigDto> trendingTabs;
  private Boolean showNewFlag;

  public void addSubTab(SportTabConfigDto tab) {
    if (subTabs == null) {
      subTabs = new ArrayList<>();
    }
    subTabs.add(tab);
  }
}
