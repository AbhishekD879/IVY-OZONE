package com.coral.oxygen.middleware.common.mappers;

import com.coral.oxygen.middleware.common.service.MarketTemplateNameService;
import com.coral.oxygen.middleware.pojos.model.output.MarketTemplateType;
import com.coral.oxygen.middleware.pojos.model.output.OutputMarket;
import com.egalacoral.spark.siteserver.model.Event;
import com.egalacoral.spark.siteserver.model.Market;

public class MarketHandicapTypeMapper extends ChainedMarketMapper {

  private MarketTemplateNameService marketTemplateNameService;

  public MarketHandicapTypeMapper(
      MarketMapper chain, MarketTemplateNameService marketTemplateNameService) {
    super(chain);
    this.marketTemplateNameService = marketTemplateNameService;
  }

  @Override
  public void populate(OutputMarket result, Event event, Market market) {
    result.setHandicapType(calculateHandicapType(market, event));
  }

  private String calculateHandicapType(Market market, Event parentEvent) {
    if ("FOOTBALL".equals(parentEvent.getCategoryCode())
        && "MH".equals(market.getMarketMeaningMinorCode())) {
      String templateMarketName = market.getTemplateMarketName();
      if (templateMarketName == null) {
        return null;
      }
      if (marketTemplateNameService.containsName(
          MarketTemplateType.HANDICAP_MATCH_RESULT, templateMarketName)) {
        return "matchResult";
      } else if (marketTemplateNameService.containsName(
          MarketTemplateType.HANDICAP_FIRST_HALF, templateMarketName)) {
        return "firstHalf";
      } else if (marketTemplateNameService.containsName(
          MarketTemplateType.HANDICAP_SECOND_HALF, templateMarketName)) {
        return "secondHalf";
      }
    }
    return null;
  }
}
