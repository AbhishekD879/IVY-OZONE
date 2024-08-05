package com.coral.oxygen.edp.model.mapping;

import com.coral.oxygen.edp.model.mapping.converter.MarketGroupAndSortConverter;
import com.coral.oxygen.edp.model.output.OutputEvent;
import com.coral.oxygen.edp.model.output.OutputMarket;
import com.coral.oxygen.edp.model.output.OutputOutcome;
import com.coral.oxygen.edp.model.output.OutputPrice;
import com.egalacoral.spark.siteserver.model.Event;
import com.egalacoral.spark.siteserver.model.Market;
import java.util.*;
import java.util.stream.Collectors;

public class SimpleEventMapper implements EventMapper {

  private final List<String> virtualRacingIds;

  private final MarketMapper marketMapper;
  private final MarketGroupAndSortConverter marketGroupAndSortConverter;

  public SimpleEventMapper(
      MarketMapper marketMapper,
      MarketGroupAndSortConverter marketGroupAndSortConverter,
      List<String> virtualRacingIds) {

    this.virtualRacingIds = virtualRacingIds;
    this.marketMapper = marketMapper;
    this.marketGroupAndSortConverter = marketGroupAndSortConverter;
  }

  @Override
  public OutputEvent map(OutputEvent result, Event event) {
    result.setId(Long.valueOf(event.getId()));
    result.setName(event.getName());
    result.setEventSortCode(event.getEventSortCode());
    result.setStartTime(event.getStartTime());
    result.setLiveServChannels(event.getLiveServChannels());
    result.setLiveServChildrenChannels(event.getLiveServChildrenChannels());
    result.setLiveServLastMsgId(event.getLiveServLastMsgId());
    result.setCategoryId(event.getCategoryId());
    result.setCategoryCode(event.getCategoryCode());
    result.setCategoryName(event.getCategoryName());
    result.setTypeName(event.getTypeName());
    result.setCashoutAvail(event.getCashoutAvail());
    result.setDisplayOrder(event.getDisplayOrder());

    result.setIsStarted(event.getIsStarted());
    result.setIsFinished(event.getIsFinished());
    result.setResponseCreationTime(event.getResponseCreationTime());
    result.setDrilldownTagNames(event.getDrilldownTagNames());
    result.setTypeId(event.getTypeId());
    result.setEventStatusCode(event.getEventStatusCode());
    result.setEventFlagCodes(event.getEventFlagCodes());

    mapMarkets(result, event);
    result.setClassId(event.getClassId());

    // outcome sorting:
    if (isRacing(result)) {
      result.getMarkets().stream()
          .findFirst()
          .ifPresent(
              market ->
                  market
                      .getOutcomes()
                      .sort(
                          Comparator.comparingDouble(this::getPrice)
                              .thenComparing(OutputOutcome::getName)));
    }

    return result;
  }

  /**
   * Get the outcome's first calculated price
   *
   * @param outcome to get price from
   * @return double value of division of num by den
   */
  private double getPrice(OutputOutcome outcome) {
    return outcome.getPrices().stream().findFirst().map(this::calculatePrice).orElse(0.0);
  }

  /**
   * @return the division of price's num by den
   */
  private double calculatePrice(OutputPrice price) {
    if (price.getPriceDen() > 0) {
      return Double.valueOf(price.getPriceNum()) / Double.valueOf(price.getPriceDen());
    } else {
      return 0;
    }
  }

  private boolean isRacing(OutputEvent event) {
    return virtualRacingIds.contains(event.getClassId());
  }

  protected void mapMarkets(OutputEvent result, Event event) {

    if (event.getMarkets() == null) {
      return;
    }
    List<OutputMarket> markets =
        event.getMarkets().stream() //
            .filter(Objects::nonNull) //
            .filter(m -> !m.getOutcomes().isEmpty())
            .map(m -> this.mapMarket(event, m)) //
            .filter(Objects::nonNull) //
            .collect(Collectors.toCollection(ArrayList::new));
    result.setMarketsCount(markets.size());

    Collection<List<OutputMarket>> groupedMarkets = marketGroupAndSortConverter.convert(markets);
    result.setMarketsByTemplateMarket(groupedMarkets);
    result.setMarkets(
        groupedMarkets.stream()
            .flatMap(List::stream)
            .collect(Collectors.toCollection(ArrayList::new)));
  }

  protected OutputMarket mapMarket(Event event, Market market) {
    return marketMapper.map(event, market);
  }
}
