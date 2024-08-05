package com.coral.oxygen.middleware.common.mappers;

import static com.coral.oxygen.middleware.pojos.model.output.MarketTemplateType.NEXT_TEAM_TO_SCORE;

import com.coral.oxygen.middleware.common.service.MarketTemplateNameService;
import com.coral.oxygen.middleware.common.utils.Converter;
import com.coral.oxygen.middleware.pojos.model.output.OutputMarket;
import com.egalacoral.spark.siteserver.model.Event;
import com.egalacoral.spark.siteserver.model.Market;
import com.google.common.collect.Iterables;
import java.util.Arrays;
import java.util.List;

public class MarketNextScoreMapper extends ChainedMarketMapper {

  private Converter<String, Integer> ordinalToNumberConverter;
  private final MarketTemplateNameService marketTemplateNameService;

  public MarketNextScoreMapper(
      MarketMapper chain,
      Converter<String, Integer> ordinalToNumberConverter,
      MarketTemplateNameService marketTemplateNameService) {
    super(chain);
    this.ordinalToNumberConverter = ordinalToNumberConverter;
    this.marketTemplateNameService = marketTemplateNameService;
  }

  @Override
  public void populate(OutputMarket result, Event event, Market market) {
    result.setNextScore(calculateNextScore(market, event));
  }

  private Integer calculateNextScore(Market market, Event parentEvent) {
    if ("FOOTBALL".equals(parentEvent.getCategoryCode())
        && marketTemplateNameService.containsName(
            NEXT_TEAM_TO_SCORE, market.getTemplateMarketName())) {

      List<String> splittedMarketName = Arrays.asList(market.getName().trim().split(" "));
      if (market.getName().matches(".*\\s\\d+$")) { // ends with number
        return Integer.parseInt(Iterables.getLast(splittedMarketName));
      } else {
        return ordinalToNumberConverter.convert(Iterables.getFirst(splittedMarketName, ""));
      }
    }
    return null;
  }
}
