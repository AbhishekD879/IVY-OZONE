package com.coral.oxygen.middleware.common.mappers;

import com.coral.oxygen.middleware.pojos.model.output.OutputMarket;
import com.coral.oxygen.middleware.pojos.model.output.OutputOutcome;
import com.egalacoral.spark.siteserver.model.Event;
import com.egalacoral.spark.siteserver.model.Market;
import com.egalacoral.spark.siteserver.model.Outcome;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Objects;
import java.util.stream.Collectors;
import lombok.extern.slf4j.Slf4j;

@Slf4j
public class SimpleMarketMapper implements MarketMapper {

  private final OutcomeMapper outcomeMapper;

  private static final String MKTFLAG_BB = "MKTFLAG_BB";
  private static final String EVFLAG_BB = "EVFLAG_BB";

  public SimpleMarketMapper(OutcomeMapper outcomeMapper) {
    this.outcomeMapper = outcomeMapper;
  }

  @Override
  public OutputMarket map(Event event, Market market) {
    OutputMarket result = new OutputMarket();

    result.setId(market.getId());
    result.setName(market.getName());
    result.setLpAvailable(market.getIsLpAvailable());
    result.setSpAvailable(market.getIsSpAvailable());
    result.setGpAvailable(market.getIsGpAvailable());
    result.setEachWayAvailable(market.getIsEachWayAvailable());
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
    result.setMarketBetInRun(market.getIsMarketBetInRun());
    result.setRawHandicapValue(market.getRawHandicapValue());
    result.setDispSortName(market.getDispSortName());
    result.setMarketStatusCode(market.getMarketStatusCode());
    result.setTemplateMarketId(market.getTemplateMarketId());
    result.setTemplateMarketName(market.getTemplateMarketName());
    result.setDrilldownTagNames(market.getDrilldownTagNames());
    result.setDisplayOrder(market.getDisplayOrder());
    result.setFlags(market.getFlags());
    result.setOutcomes(
        market.getOutcomes().stream()
            .filter(Objects::nonNull)
            .map(o -> this.mapOutcome(event, market, o))
            .collect(Collectors.toCollection(ArrayList::new)));
    if (Objects.nonNull(market.getExtIds()) && getDrillDownBBFlag(event, market)) {
      result.setBybAvailableMarket(true);
    }
    if (Objects.nonNull(market.getExtIds())) {
      List<String> extId = Arrays.asList(market.getExtIds().split(","));
      result.setBwinId(extId.get(1));
    }
    return result;
  }

  private static boolean getDrillDownBBFlag(Event event, Market market) {
    return (Objects.nonNull(market.getDrilldownTagNames())
            && market.getDrilldownTagNames().contains(MKTFLAG_BB))
        && (Objects.nonNull(event.getDrilldownTagNames())
            && event.getDrilldownTagNames().contains(EVFLAG_BB));
  }

  protected OutputOutcome mapOutcome(Event event, Market market, Outcome outcome) {
    return outcomeMapper.map(event, market, outcome);
  }
}
