package com.ladbrokescoral.oxygen.cms.api.controller.dto;

import com.ladbrokescoral.oxygen.cms.api.entity.InitialBanner;
import com.ladbrokescoral.oxygen.cms.api.entity.TrendingTab;
import java.util.LinkedHashSet;
import java.util.List;
import javax.validation.constraints.NotBlank;
import javax.validation.constraints.NotNull;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@Builder
@AllArgsConstructor
@NoArgsConstructor
public class SportTabInputDto {
  @NotBlank private String brand;
  @NotNull private Integer sportId;
  @NotBlank private String name;
  @NotBlank private String displayName;
  private Filters filters;
  private boolean enabled;
  private boolean checkEvents;
  private boolean hasEvents;
  private Double sortOrder;
  private LinkedHashSet<SportTabMarketDto> marketsNames = new LinkedHashSet<>();
  private InitialBanner interstitialBanners;

  private List<TrendingTab> trendingTabs;
  private Boolean showNewFlag;
}
