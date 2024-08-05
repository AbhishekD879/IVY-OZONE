package com.ladbrokescoral.oxygen.cms.api.dto;

import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonInclude.Include;
import java.util.List;
import java.util.Map;
import lombok.Data;

@Data
public class InitialDataDto {
  @JsonInclude(Include.NON_NULL)
  private List<BannerDto> banners;

  @JsonInclude(Include.NON_EMPTY)
  private List<InitialDataSportCategoryDto> sportCategories;

  private List<InitialDataSportDto> sports;
  private List<BaseModularContentDto> modularContent;
  private Map<String, String> seoPages;
  private List<InitialDataFooterMenuV2Dto> footerMenu;
  private List<InitSignpostingDto> initSignposting;
  private Map<String, Map<String, Object>> systemConfiguration;
  private List<NavigationPointDto> navigationPoints;
  private List<ExtraNavigationPointPublicDto> extraNavigationPoints;
  private List<ConnectMenuDto> connectMenu;
  private OddsBoostConfigDTO oddsBoost;
  private QuizPopupSettingDto quizPopupSetting;
  private List<VirtualSportAliasesDto> vsAliases;
  private String svgSpriteContent;
  private TimelineGeneralConfigDto timelineConfig;
  private Map<String, SeoAutoInitDataDto> seoAutoPages;
  private List<InitialLuckyDipConfigDto> luckyDipConfigs;
}
