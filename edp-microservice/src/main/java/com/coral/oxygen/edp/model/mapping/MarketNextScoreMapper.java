package com.coral.oxygen.edp.model.mapping;

import com.coral.oxygen.edp.model.mapping.converter.Converter;
import com.coral.oxygen.edp.model.output.OutputMarket;
import com.egalacoral.spark.siteserver.model.Event;
import com.egalacoral.spark.siteserver.model.Market;
import com.google.common.collect.Iterables;
import java.util.Arrays;
import java.util.List;
import lombok.extern.slf4j.Slf4j;

@Slf4j
public class MarketNextScoreMapper extends ChainedMarketMapper {

  private Converter<String, Integer> ordinalToNumberConverter;

  public MarketNextScoreMapper(
      MarketMapper chain, Converter<String, Integer> ordinalToNumberConverter) {
    super(chain);
    this.ordinalToNumberConverter = ordinalToNumberConverter;
  }

  @Override
  public void populate(OutputMarket result, Event event, Market market) {
    result.setNextScore(calculateNextScore(market, event));
  }

  private Integer calculateNextScore(Market market, Event parentEvent) {
    if ("FOOTBALL".equals(parentEvent.getCategoryCode())
        && "Next Team to Score".equals(market.getTemplateMarketName())) {

      if (market.getName() == null) {
        return null;
      }

      List<String> splittedMarketName = Arrays.asList(market.getName().trim().split(" "));

      final String regex = ".*\\s\\d+$";
      if (market.getName().matches(regex)) { // ends with number
        try {
          return Integer.parseInt(Iterables.getLast(splittedMarketName));
        } catch (NumberFormatException e) {
          log.error("error in calculating nextScore", e);
        }
      } else {
        return ordinalToNumberConverter.convert(Iterables.getFirst(splittedMarketName, ""));
      }
    }
    return null;
  }
}
