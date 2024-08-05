package com.coral.oxygen.middleware.in_play.service.market.selector;

import java.util.Arrays;
import java.util.Collections;
import java.util.List;

public class MarketSelectorConstants {

  private MarketSelectorConstants() {}

  public static final String PRIMARY_MARKETS = "PRIMARY_MARKETS";
  public static final String SIMPLE_MARKET = "SIMPLE_MARKET";
  public static final String RAW_HANDICAP_VALUE_MARKET = "RAW_HANDICAP_VALUE_MARKET";
  public static final String MARKET_WITH_MULTIPLE_NAMES = "MARKET_WITH_MULTIPLE_NAMES";
  public static final String DEFAULT_MARKETS = "DEFAULT_MARKETS";
  public static final String FAVOURITE_MARKET_SELECTOR = "FAVOURITE_MARKET_SELECTOR";
  public static final String DELIMETER = ",";
  public static final String MARKET_SWITCHER_SELECTIONS_JSON = "marketSwitcherSelections.json";
  public static final List<String> SWITCHER_ENABLED_SPORTS =
      Collections.unmodifiableList(Arrays.asList("FOOTBALL", "TENNIS", "BASKETBALL"));
  public static final List<String> TIER_TWO_SPORTS =
      Collections.unmodifiableList(Arrays.asList("RUGBY_UNION", "RUGBY_LEAGUE", "AMERICAN_FB"));
}
