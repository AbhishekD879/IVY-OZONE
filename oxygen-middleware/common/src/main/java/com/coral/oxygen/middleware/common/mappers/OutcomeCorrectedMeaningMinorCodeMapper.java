package com.coral.oxygen.middleware.common.mappers;

import com.coral.oxygen.middleware.common.service.SportsConfig;
import com.coral.oxygen.middleware.pojos.model.output.OutputOutcome;
import com.egalacoral.spark.siteserver.model.Event;
import com.egalacoral.spark.siteserver.model.Market;
import com.egalacoral.spark.siteserver.model.Outcome;
import java.util.stream.Collectors;

public class OutcomeCorrectedMeaningMinorCodeMapper extends ChainedOutcomeMapper {

  private static final int TWO = 2;
  private final SportsConfig sportsConfig;

  public OutcomeCorrectedMeaningMinorCodeMapper(
      OutcomeMapper outcomeMapper, SportsConfig sportsConfig) {
    super(outcomeMapper);
    this.sportsConfig = sportsConfig;
  }

  @Override
  protected void populate(OutputOutcome result, Event event, Market market, Outcome outcome) {
    String categoryId = event.getCategoryId();
    if (!isRacing(categoryId)) {
      result.setCorrectedOutcomeMeaningMinorCode(
          calculateCorrectedOutcomeMeaningMinorCode(
              outcome, market, EventIsUSMapper.calculateIsUS(event)));
    }
  }

  private boolean isRacing(String sportId) {
    SportsConfig.SportConfigItem sConfig = sportsConfig.getBySportId(sportId);
    return sConfig != null && sConfig.isRacing();
  }

  private int calculateCorrectedOutcomeMeaningMinorCode(
      Outcome outcome, Market market, boolean isUS) {
    String outcomeMeaningMinorCode = outcome.getOutcomeMeaningMinorCode();
    try {
      return Integer.parseInt(outcomeMeaningMinorCode);
    } catch (Exception e) {
      if (outcomeMeaningMinorCode == null) {
        outcomeMeaningMinorCode = "";
      }
      int result =
          correctMeaningMinorCodeForUsMarkets(market, outcome, isUS, outcomeMeaningMinorCode);
      result = correctMeaningMinorCodeForYesOrNoMarkets(outcome, result, isUS);
      return result;
    }
  }

  private int correctMeaningMinorCodeForUsMarkets(
      Market market, Outcome outcome, boolean isUS, String outcomeMeaningMinorCode) {
    int position =
        market.getOutcomes().stream()
                .map(Outcome::getId)
                .sorted()
                .collect(Collectors.toList())
                .indexOf(outcome.getId())
            + 1;
    int noOfOutcomes = market.getOutcomes().size();
    int result;
    switch (outcomeMeaningMinorCode) {
      case "H":
        result = isUS ? 3 : 1;
        break;
      case "D":
      case "N":
      case "L":
        result = 2;
        break;
      case "A":
        result = isUS ? 1 : 3;
        break;
      default:
        if (noOfOutcomes == TWO && position == TWO) {
          result = 3;
        } else result = position;
        break;
    }

    return result;
  }

  private int correctMeaningMinorCodeForYesOrNoMarkets(Outcome outcome, int result, boolean isUS) {
    if ("HL".equals(outcome.getOutcomeMeaningMajorCode())
        && "L".equals(outcome.getOutcomeMeaningMinorCode())) {
      result = isUS ? 1 : 3;
    }
    // checking for outcome from 'Both teams to score market'
    if ("Yes".equalsIgnoreCase(outcome.getName())) {
      result = 1;
    }
    if ("No".equalsIgnoreCase(outcome.getName())) {
      result = 3;
    }
    return result;
  }
}
