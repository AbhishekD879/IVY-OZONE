package com.coral.oxygen.middleware.common.mappers;

import com.coral.oxygen.middleware.common.service.MarketTemplateNameService;
import com.coral.oxygen.middleware.pojos.model.output.EventsModuleData;
import com.coral.oxygen.middleware.pojos.model.output.OutputMarket;
import com.coral.oxygen.middleware.pojos.model.output.PrimaryMarkets;
import com.egalacoral.spark.siteserver.model.Event;
import java.util.*;

/** Created by azayats on 17.03.17. */
public class FeaturedSimpleEventMapper extends SimpleEventMapper {

  private MarketTemplateNameService marketTemplateNameService;

  public FeaturedSimpleEventMapper(
      MarketMapper marketMapper, MarketTemplateNameService marketTemplateNameService) {
    super(marketMapper);
    this.marketTemplateNameService = marketTemplateNameService;
  }

  @Override
  protected void mapMarkets(EventsModuleData result, Event event) {
    // temporary fix to have only one market with the lowest display order (PHX-315)
    // will be reimplemented in future

    if (Objects.nonNull(result.getOutcomeId())) {
      // PHX-487
      // we should not avoid additional markets for single selections mapping becouse we
      // can receive few markets with different outcomes for one event from SiteServer
      super.mapMarkets(result, event);
    } else {
      List<OutputMarket> primaryMarkets = popEventIdToPRMarket(event);
      result.setPrimaryMarkets(primaryMarkets);
      if (!primaryMarkets.isEmpty()) {
        result.setMarkets(Collections.singletonList(primaryMarkets.get(0)));
      } else {
        result.setMarkets(Collections.emptyList());
      }
    }
  }

  private List<OutputMarket> popEventIdToPRMarket(Event event) {
    List<OutputMarket> prMarkets = new ArrayList<>();
    if (event.getMarkets().isEmpty()) {
      return prMarkets;
    }
    event
        .getMarkets()
        .forEach(
            market -> {
              // BMA-29915
              if (!Boolean.TRUE.equals(event.getIsLiveNowEvent())
                  || Boolean.TRUE.equals(market.getIsMarketBetInRun())) {
                prMarkets.add(mapMarket(event, market));
              }
            });
    final PrimaryMarkets prMarketConfig = PrimaryMarkets.enumerize(event.getCategoryCode());
    if (prMarketConfig != null) {
      prMarkets.sort(
          Comparator.comparingInt(
              market -> getPrimaryMarketOrderIndex(prMarketConfig, market.getName())));
    } else {
      prMarkets.sort(
          Comparator.comparing(
                  OutputMarket::getDisplayOrder, Comparator.nullsFirst(Comparator.reverseOrder()))
              .reversed());
    }
    return prMarkets;
  }

  private int getPrimaryMarketOrderIndex(PrimaryMarkets prMarketConfig, String marketName) {
    return prMarketConfig.getOrderIndex(marketTemplateNameService.getType(marketName));
  }
}
