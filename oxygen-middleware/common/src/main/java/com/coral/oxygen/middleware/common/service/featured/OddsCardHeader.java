package com.coral.oxygen.middleware.common.service.featured;

import static com.coral.oxygen.middleware.common.service.OddsCardHeaderType.homeDrawAwayType;
import static com.coral.oxygen.middleware.common.service.OddsCardHeaderType.oneThreeType;
import static com.coral.oxygen.middleware.common.service.OddsCardHeaderType.oneTwoType;

import com.coral.oxygen.middleware.common.service.OddsCardHeaderType;
import com.coral.oxygen.middleware.common.service.OutrightsConfig;
import com.coral.oxygen.middleware.common.service.SportsConfig;
import com.coral.oxygen.middleware.pojos.model.output.EventsModuleData;
import com.coral.oxygen.middleware.pojos.model.output.OutputMarket;
import java.util.Arrays;
import java.util.HashSet;
import java.util.List;
import java.util.Optional;
import java.util.Set;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

@Component
public class OddsCardHeader {

  private SportsConfig sportsConfig;

  private OutrightsConfig outrightsConfig;

  private static final Set<String> overUndeMeaningMajorCodes = new HashSet<>();
  private static final Set<String> matchResultMeaningCodes = new HashSet<>();
  private static final Set<String> yesNoDispSortNames = new HashSet<>();

  static {
    overUndeMeaningMajorCodes.add("L");
    overUndeMeaningMajorCodes.add("I");

    matchResultMeaningCodes.add("-|MR");
    matchResultMeaningCodes.add("-|H1");
    matchResultMeaningCodes.add("-|H2");

    yesNoDispSortNames.add("BO");
    yesNoDispSortNames.add("GB");
  }

  protected static final List<String> L_1_2 = Arrays.asList("1", "2");
  protected static final List<String> L_1_2_3 = Arrays.asList("1", "2", "3");
  protected static final List<String> L_YES_NO = Arrays.asList("yes", "no");
  protected static final List<String> L_OVER_UNDER = Arrays.asList("over", "under");
  protected static final List<String> L_HOME_DRAW_AWAY = Arrays.asList("home", "draw", "away");
  protected static final List<String> L_HOME_AWAY = Arrays.asList("home", "away");

  /**
   * Returns odds Card Header Type
   *
   * @param events
   * @param sportName
   * @returns {OddsCardHeaderType}
   */
  private OddsCardHeaderType getOddsCardHeader(
      List<? extends EventsModuleData> events, String sportName) {
    for (EventsModuleData event : events) {
      if (!event.getMarkets().isEmpty()
          && !event.getMarkets().get(0).getOutcomes().isEmpty()
          && "football".equalsIgnoreCase(sportName)) {
        return homeDrawAwayType;
      }

      if (!event.getMarkets().isEmpty() && event.getMarkets().get(0).getOutcomes().size() == 3) {
        return "golf".equalsIgnoreCase(sportName) ? oneThreeType : homeDrawAwayType;
      }
    }

    return oneTwoType;
  }

  /**
   * @param sportId for strict checking of sport
   * @returns {boolean}
   */
  private boolean isRacing(String sportId) {
    SportsConfig.SportConfigItem sConfig = sportsConfig.getBySportId(sportId);
    return sConfig != null && sConfig.isRacing();
  }

  // function checks is outright sport
  private boolean isOutrightSport(String code, String sportName) {
    return outrightsConfig.getOutrightsSports().contains(code)
        || (sportsConfig.getByName(sportName).isOutrightSport());
  }

  private boolean isSpecialSection(List<? extends EventsModuleData> data, String sportName) {

    // Checks if event - OutRight.
    List<String> sortCodeList;

    EventsModuleData eventEntity = data.get(0);

    if (isOutrightSport(eventEntity.getCategoryCode(), sportName)) {
      sortCodeList = outrightsConfig.getOutrightsSportSortCode();
    } else {
      sortCodeList = outrightsConfig.getSportSortCode();
    }

    // Checks if event - Enhance Multiples.
    SportsConfig.SportConfigItem sConfig = sportsConfig.getByName(sportName);
    boolean isEnhanceMultiples =
        sConfig != null
            && sportsConfig
                .getByName(sportName)
                .getSpecialsTypeIds()
                .contains(eventEntity.getTypeId());

    boolean allEventsAreOutright =
        data.stream().allMatch(e -> sortCodeList.contains(e.getEventSortCode()));

    // check if event special (Enhance Multiples or OutRight).
    return isEnhanceMultiples || allEventsAreOutright;
  }

  private OddsCardHeaderType calculateOddsCardHeaderType(
      List<? extends EventsModuleData> eventsModuleData) {
    if (eventsModuleData.isEmpty()) {
      return null;
    }
    String sportName = eventsModuleData.get(0).getCategoryName().replaceAll("\\s|\\/|\\/", "");
    String sportId = eventsModuleData.get(0).getCategoryId();

    boolean isSpecialEvent = isRacing(sportId) || isSpecialSection(eventsModuleData, sportName);
    if (isSpecialEvent) {
      return null;
    }
    if (sportsConfig.getByName(sportName).isMultiTemplateSport()) {
      return getOddsCardHeader(eventsModuleData, sportName);
    } else if (sportsConfig.getByName(sportName) != null
        && sportsConfig.getByName(sportName).getOddsCardHeaderType() != null) {
      return sportsConfig.getByName(sportName).getOddsCardHeaderType();
    } else {
      return getOddsCardHeader(eventsModuleData, sportName);
    }
  }

  private boolean isOverUnderType(OutputMarket marketEntity) {
    return overUndeMeaningMajorCodes.contains(marketEntity.getMarketMeaningMajorCode());
  }

  private String combineMeaningCode(OutputMarket marketEntity) {
    return marketEntity.getMarketMeaningMajorCode()
        + "|"
        + marketEntity.getMarketMeaningMinorCode();
  }

  private boolean isMatchResultType(OutputMarket marketEntity) {
    return matchResultMeaningCodes.contains(combineMeaningCode(marketEntity));
  }

  private boolean hasEventsAreMatchResultType(List<? extends EventsModuleData> events) {
    return events.stream()
        .anyMatch(event -> event.getMarkets().stream().anyMatch(this::isMatchResultType));
  }

  private boolean isYesNoType(OutputMarket marketEntity) {
    return yesNoDispSortNames.contains(marketEntity.getDispSortName());
  }

  public List<String> calculateHeadTitles(List<? extends EventsModuleData> moduleData) {
    Optional<OutputMarket> any =
        moduleData.stream()
            .map(EventsModuleData::getMarkets)
            .filter(markets -> !markets.isEmpty())
            .map(markets -> markets.get(0))
            .findAny();
    OutputMarket marketEntity = null;
    boolean isOverUnderType = false;
    boolean isMatchResultType = false;
    boolean isYesNoType = false;
    if (any.isPresent()) {
      marketEntity = any.get();
      isOverUnderType = isOverUnderType(marketEntity);
      isMatchResultType = hasEventsAreMatchResultType(moduleData);
      isYesNoType = isYesNoType(marketEntity);
    }
    OddsCardHeaderType oddsCardHeader = calculateOddsCardHeaderType(moduleData);
    if (oneThreeType.equals(oddsCardHeader)) {
      return L_1_2_3;
    } else if (oneTwoType.equals(oddsCardHeader)) {
      return L_1_2;
    } else if (homeDrawAwayType.equals(oddsCardHeader)
        && marketEntity != null
        && !isMatchResultType
        && isYesNoType) {
      return L_YES_NO;
    } else if (homeDrawAwayType.equals(oddsCardHeader)
        && marketEntity != null
        && !isMatchResultType
        && isOverUnderType) {
      return L_OVER_UNDER;
    } else if (homeDrawAwayType.equals(oddsCardHeader)
        && (marketEntity != null && !isMatchResultType)
        && !isOverUnderType
        && !isYesNoType) {
      return L_HOME_AWAY;
    } else if (homeDrawAwayType.equals(oddsCardHeader)
        && (isMatchResultType || marketEntity == null)) {
      return L_HOME_DRAW_AWAY;
    }
    return null;
  }

  @Autowired
  public void setSportsConfig(SportsConfig sportsConfig) {
    this.sportsConfig = sportsConfig;
  }

  @Autowired
  public void setOutrightsConfig(OutrightsConfig outrightsConfig) {
    this.outrightsConfig = outrightsConfig;
  }
}
