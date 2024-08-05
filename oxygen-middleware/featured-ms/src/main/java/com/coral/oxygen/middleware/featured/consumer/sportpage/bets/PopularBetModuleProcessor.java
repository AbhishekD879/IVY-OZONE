package com.coral.oxygen.middleware.featured.consumer.sportpage.bets;

import com.coral.oxygen.middleware.featured.consumer.sportpage.ModuleConsumer;
import com.coral.oxygen.middleware.featured.service.PopularBetService;
import com.coral.oxygen.middleware.pojos.model.cms.featured.PopularBet;
import com.coral.oxygen.middleware.pojos.model.cms.featured.SportPageModule;
import com.coral.oxygen.middleware.pojos.model.output.EventsModuleData;
import com.coral.oxygen.middleware.pojos.model.output.featured.PopularBetModule;
import com.coral.oxygen.middleware.pojos.model.output.featured.PopularBetModuleData;
import com.coral.oxygen.middleware.pojos.model.output.popular_bet.TrendingBetsDto;
import com.coral.oxygen.middleware.pojos.model.output.popular_bet.TrendingPosition;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.stream.Collectors;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Slf4j
@Service
public class PopularBetModuleProcessor implements ModuleConsumer<PopularBetModule> {

  public static final String FOOTBALL_TB_H_H = "football_tb_%sh_%sh";
  private final PopularBetService popularBetService;

  @Autowired
  public PopularBetModuleProcessor(PopularBetService popularBetService) {
    this.popularBetService = popularBetService;
  }

  public List<PopularBetModule> processModules(SportPageModule sportPageModule) {
    try {
      log.info("popular bets module processing started");
      return sportPageModule.getPageData().stream()
          .filter(PopularBet.class::isInstance)
          .map(PopularBet.class::cast)
          .map(this::toPopularBetModule)
          .collect(Collectors.toCollection(ArrayList::new));

    } catch (Exception e) {
      log.error("PopularBetModuleProcessor -> ", e);
      return Collections.emptyList();
    }
  }

  protected PopularBetModule toPopularBetModule(PopularBet popularBet) {
    PopularBetModule popularBetModule = new PopularBetModule();

    mapPopularBetModuleConfig(popularBetModule, popularBet);
    popularBetModule.setId(popularBet.getId());
    // inject trending bets data
    popularBetModule.setData(getPopularBetApiInformation(popularBetModule));
    return popularBetModule;
  }

  private List<EventsModuleData> getPopularBetApiInformation(PopularBetModule popularBetModule) {
    try {

      // starts in 48h first backed in second field . football is constant
      TrendingBetsDto dto =
          popularBetService.getTrendingBetByChannel(
              String.format(
                  FOOTBALL_TB_H_H,
                  popularBetModule.getMostBackedIn(),
                  popularBetModule.getEventStartsIn()));
      popularBetModule.setLastMsgUpdatedAt(dto.getLastMsgUpdatedAt());
      popularBetModule.setUpdatedAt(dto.getUpdatedAt());

      // inject event data.
      return dto.getPositions().stream().map(this::mapMetaData).collect(Collectors.toList());

    } catch (Exception ex) {
      log.info("trending bets ms call failed with reason {}", ex);
    }
    return Collections.emptyList();
  }

  private PopularBetModuleData mapMetaData(TrendingPosition position) {
    PopularBetModuleData data = position.getEvent();
    data.setNBets(position.getNBets());
    data.setRank(position.getRank());
    data.setPreviousRank(position.getPreviousRank());
    data.setPosition(position.getPosition());
    return data;
  }

  /**
   * This method used to reduce duplicate code for Fanzone HighlightCarouselModule and Existing
   * HighlightCarouselModule process
   *
   * @param popularBetModule it is HighlightCarouselModule mapped from CMS module
   * @param popularBet it is CMS module
   */
  protected void mapPopularBetModuleConfig(
      PopularBetModule popularBetModule, PopularBet popularBet) {
    popularBetModule.setId(popularBet.getId());
    popularBetModule.setSportId(popularBet.getSportId());
    mapToConfig(popularBetModule, popularBet);
  }

  private static void mapToConfig(PopularBetModule popularBetModule, PopularBet popularBet) {
    if (popularBet.getPopularBetConfig() != null) {
      popularBetModule.setRedirectionUrl(popularBet.getPopularBetConfig().getRedirectionUrl());
      popularBetModule.setDisplayName(popularBet.getPopularBetConfig().getDisplayName());
      popularBetModule.setMostBackedIn(popularBet.getPopularBetConfig().getMostBackedIn());
      popularBetModule.setEventStartsIn(popularBet.getPopularBetConfig().getEventStartsIn());
      popularBetModule.setPriceRange(popularBet.getPopularBetConfig().getPriceRange());
      popularBetModule.setMaxSelections(popularBet.getPopularBetConfig().getMaxSelections());
      popularBetModule.setEnableBackedInTimes(
          popularBet.getPopularBetConfig().isEnableBackedInTimes());
    }
  }
}
