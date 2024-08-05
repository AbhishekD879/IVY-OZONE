package com.coral.oxygen.edp.model.mapping;

import com.coral.oxygen.edp.model.output.OutputMarket;
import com.coral.oxygen.edp.model.output.OutputOutcome;
import com.egalacoral.spark.siteserver.model.Event;
import com.egalacoral.spark.siteserver.model.Market;
import com.egalacoral.spark.siteserver.model.Outcome;
import java.util.ArrayList;
import java.util.Objects;
import java.util.stream.Collectors;

public class SimpleMarketMapper implements MarketMapper {

  private final OutcomeMapper outcomeMapper;

  public SimpleMarketMapper(OutcomeMapper outcomeMapper) {
    this.outcomeMapper = outcomeMapper;
  }

  @Override
  public OutputMarket map(Event event, Market market) {
    OutputMarket result = new OutputMarket();

    result.setId(market.getId());
    result.setName(market.getName());
    result.setIsLpAvailable(market.getIsLpAvailable());
    result.setIsSpAvailable(market.getIsSpAvailable());
    result.setIsGpAvailable(market.getIsGpAvailable());
    result.setEachWayFactorNum(market.getEachWayFactorNum());
    result.setEachWayFactorDen(market.getEachWayFactorDen());
    result.setEachWayPlaces(market.getEachWayPlaces());
    result.setLiveServChannels(market.getLiveServChannels());
    result.setPriceTypeCodes(
        market.getPriceTypeCodes() != null
                && market.getPriceTypeCodes().charAt(market.getPriceTypeCodes().length() - 1) == ','
            ? market.getPriceTypeCodes().substring(0, market.getPriceTypeCodes().length() - 1)
            : market.getPriceTypeCodes());
    result.setNcastTypeCodes(market.getNcastTypeCodes());
    result.setCashoutAvail(market.getCashoutAvail());
    result.setMarketMeaningMajorCode(market.getMarketMeaningMajorCode());
    result.setMarketMeaningMinorCode(market.getMarketMeaningMinorCode());
    result.setIsMarketBetInRun(market.getIsMarketBetInRun());
    result.setRawHandicapValue(market.getRawHandicapValue());
    result.setDispSortName(market.getDispSortName());
    result.setMarketStatusCode(market.getMarketStatusCode());
    result.setTemplateMarketId(market.getTemplateMarketId());
    result.setTemplateMarketName(market.getTemplateMarketName());
    result.setDrilldownTagNames(market.getDrilldownTagNames());
    result.setDisplayOrder(market.getDisplayOrder());
    result.setIsEachWayAvailable(market.getIsEachWayAvailable());
    result.setFlags(market.getFlags());

    result.setOutcomes(
        market.getOutcomes().stream() //
            .filter(Objects::nonNull)
            .map(o -> this.mapOutcome(event, market, o)) //
            .collect(Collectors.toCollection(ArrayList::new)));

    return result;
  }

  private OutputOutcome mapOutcome(Event event, Market market, Outcome outcome) {
    return outcomeMapper.map(event, market, outcome);
  }
}
