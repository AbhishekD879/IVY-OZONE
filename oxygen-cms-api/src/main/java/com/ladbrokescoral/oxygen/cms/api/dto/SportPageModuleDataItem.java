package com.ladbrokescoral.oxygen.cms.api.dto;

import com.fasterxml.jackson.annotation.JsonIgnore;
import com.fasterxml.jackson.annotation.JsonSubTypes;
import com.fasterxml.jackson.annotation.JsonTypeInfo;

@JsonTypeInfo(use = JsonTypeInfo.Id.NAME, property = "@type")
@JsonSubTypes({
  @JsonSubTypes.Type(value = ModularIdsContentDto.class, name = "FEATURED"),
  @JsonSubTypes.Type(value = ModularContentDto.class, name = "COMMON_MODULE"),
  @JsonSubTypes.Type(value = SportQuickLinkDto.class, name = "QUICK_LINK"),
  @JsonSubTypes.Type(value = InPlayConfigDto.class, name = "IN_PLAY"),
  @JsonSubTypes.Type(value = RecentlyPlayedGameDto.class, name = "RECENTLY_PLAYED_GAMES"),
  @JsonSubTypes.Type(value = HighlightCarouselDto.class, name = "HIGHLIGHTS_CAROUSEL"),
  @JsonSubTypes.Type(value = SurfaceBetDto.class, name = "SURFACE_BET"),
  @JsonSubTypes.Type(value = AemBannersDto.class, name = "AEM_BANNERS"),
  @JsonSubTypes.Type(value = RacingModuleDto.class, name = "RACING_MODULE"),
  @JsonSubTypes.Type(value = VirtualNextEventDto.class, name = "VIRTUAL_NEXT_EVENTS"),
  @JsonSubTypes.Type(value = TeamBetsDto.class, name = "BETS_BASED_ON_YOUR_TEAM"),
  @JsonSubTypes.Type(value = FanBetsDto.class, name = "BETS_BASED_ON_OTHER_FANS"),
  @JsonSubTypes.Type(value = PopularBetDto.class, name = "POPULAR_BETS"),
  @JsonSubTypes.Type(value = BybWidgetModuleDto.class, name = "BYB_WIDGET"),
  @JsonSubTypes.Type(value = LuckyDipModuleDto.class, name = "LUCKY_DIP"),
  @JsonSubTypes.Type(value = SuperButtonDto.class, name = "SUPER_BUTTON"),
  @JsonSubTypes.Type(value = PopularAccaModuleDto.class, name = "POPULAR_ACCA")
})
public interface SportPageModuleDataItem {

  @JsonIgnore
  SportPageId sportPageId();
}
