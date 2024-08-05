package com.coral.oxygen.edp.model.mapping;

import com.coral.oxygen.edp.model.mapping.config.SportsConfig;
import com.coral.oxygen.edp.model.output.OutputOutcome;
import com.egalacoral.spark.siteserver.model.Event;
import com.egalacoral.spark.siteserver.model.Market;
import com.egalacoral.spark.siteserver.model.Outcome;

public class OutcomeCorrectedMeaningMinorCodeMapper extends ChainedOutcomeMapper {

  private final SportsConfig sportsConfig;

  private static final int ONE = 1;
  private static final int TWO = 2;
  private static final int THREE = 3;

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
          tryParseCorrectedOutcomeMeaningMinorCode(outcome, event));
    }
  }

  private boolean isRacing(String sportId) {
    SportsConfig.SportConfigItem sConfig = sportsConfig.getBySportId(sportId);
    return sConfig != null && sConfig.isRacing();
  }

  private Integer tryParseCorrectedOutcomeMeaningMinorCode(Outcome outcome, Event event) {
    try {
      return Integer.parseInt(outcome.getOutcomeMeaningMinorCode());
    } catch (NumberFormatException e) {
      return parseCorrectedOutcomeMeaningMinorCode(outcome, event);
    }
  }

  private Integer parseCorrectedOutcomeMeaningMinorCode(Outcome outcome, Event event) {
    Integer result = parseMeaningMinorCode(outcome, event);

    String outcomeMeaningMajorCode = outcome.getOutcomeMeaningMajorCode();
    if ("HL".equals(outcomeMeaningMajorCode) && "L".equals(outcome.getOutcomeMeaningMinorCode())) {
      result = THREE;
    }

    // checking for outcome from 'Both teams to score market'
    if ("--".equals(outcomeMeaningMajorCode) && "Yes".equalsIgnoreCase(outcome.getName())) {
      result = ONE;
    }
    if ("--".equals(outcomeMeaningMajorCode) && "No".equalsIgnoreCase(outcome.getName())) {
      result = THREE;
    }
    return result;
  }

  private Integer parseMeaningMinorCode(Outcome outcome, Event event) {
    String outcomeMeaningMinorCode = outcome.getOutcomeMeaningMinorCode();
    if (outcomeMeaningMinorCode == null) {
      outcomeMeaningMinorCode = "";
    }
    boolean isUS = EventIsUSMapper.calculateIsUS(event);
    int result;
    switch (outcomeMeaningMinorCode) {
      case "H":
        result = isUS ? THREE : ONE;
        break;
      case "D":
      case "N":
      case "L":
        result = TWO;
        break;
      case "A":
        result = isUS ? ONE : THREE;
        break;
      default:
        String outcomeName = outcome.getName();
        String eventName = event.getName();

        if (eventName == null) return null;

        String homeTeamName = parseFirstTeamName(eventName);
        // outcomes with name 'Yes' or name of home team should be ordered first
        boolean isFirst =
            "yes".equalsIgnoreCase(outcomeName) || (homeTeamName.equalsIgnoreCase(outcomeName));

        result = isFirst ? ONE : THREE;
    }
    return result;
  }

  private String parseFirstTeamName(String eventName) {
    int separatorIndex = eventName.indexOf(" vs ");
    if (separatorIndex < 0) {
      separatorIndex = eventName.indexOf(" v ");
    }
    if (separatorIndex < 0) {
      separatorIndex = eventName.indexOf(" @ ");
    }
    if (separatorIndex < 0) {
      separatorIndex = eventName.indexOf('/');
    }
    if (separatorIndex < 0) {
      return "";
    }
    return eventName.substring(0, separatorIndex).trim();
  }
}
