package com.ladbrokescoral.oxygen.cms.api.service.sporttab;

import com.ladbrokescoral.oxygen.cms.api.entity.SportCategory;
import com.ladbrokescoral.oxygen.cms.api.entity.SportTab;
import com.ladbrokescoral.oxygen.cms.api.entity.SportTier;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import org.springframework.stereotype.Component;

@Component
public class Tier2SportTabsTemplate extends SportTabsTemplate {

  private static final List<SportTab> TIER_2_TABS = new ArrayList<>();
  private static final Map<String, String> MATCHES_TAB_DISP_NAME = new HashMap<>();

  private static final String DEFAULT_MATCHES_DISP_NAME = "Matches";
  private static final String EVENTS = "Events";
  private static final String FIGHTS = "Fights";

  private static final double GOLF_MATCHES_SORT_ORDER = 6.0;

  private static final double GOLF_INPLAY_MATCHES_SORT_ORDER = 7.0;
  private static final String DEFAULT_GOLF_INPLAY_DISP_NAME = "In-Play";

  private static final List<SportTab> TIER_2_GOLF_TABS = new ArrayList<>();

  static {
    // MATCHES adds per sport with Sort order 1.0
    TIER_2_TABS.add(
        createTab(SportTabNames.COMPETITIONS.nameLowerCase(), "Competitions", 2.0, true, true));
    TIER_2_TABS.add(
        createTab(SportTabNames.OUTRIGHTS.nameLowerCase(), "Outrights", 3.0, true, true));
    TIER_2_TABS.add(createTab(SportTabNames.COUPONS.nameLowerCase(), "Coupons", 4.0, false, false));
    TIER_2_TABS.add(createTab(SportTabNames.SPECIALS.nameLowerCase(), "Specials", 5.0, true, true));

    TIER_2_GOLF_TABS.addAll(TIER_2_TABS);
    TIER_2_GOLF_TABS.add(
        createTab(
            SportTabNames.GOLF_MATCHES.nameLowerCase(),
            DEFAULT_MATCHES_DISP_NAME,
            GOLF_MATCHES_SORT_ORDER,
            true,
            true));
    TIER_2_GOLF_TABS.add(
        createTab(
            SportTabNames.LIVE.nameLowerCase(),
            DEFAULT_GOLF_INPLAY_DISP_NAME,
            GOLF_INPLAY_MATCHES_SORT_ORDER,
            true,
            true));

    MATCHES_TAB_DISP_NAME.put("ATHLETICS", EVENTS);
    MATCHES_TAB_DISP_NAME.put("BOXING", FIGHTS);
    MATCHES_TAB_DISP_NAME.put("CURLING", EVENTS);
    MATCHES_TAB_DISP_NAME.put("CYCLING", EVENTS);
    MATCHES_TAB_DISP_NAME.put("ESPORTS", EVENTS);
    MATCHES_TAB_DISP_NAME.put("MOTOR_CARS", EVENTS);
    MATCHES_TAB_DISP_NAME.put("GOLF", EVENTS);
    MATCHES_TAB_DISP_NAME.put("MOTOR_BIKES", EVENTS);
    MATCHES_TAB_DISP_NAME.put("MOTOR_SPORTS", EVENTS);
    MATCHES_TAB_DISP_NAME.put("NETBALL", EVENTS);
    MATCHES_TAB_DISP_NAME.put("POLITICS", EVENTS);
    MATCHES_TAB_DISP_NAME.put("ROWING", EVENTS);
    MATCHES_TAB_DISP_NAME.put("9", EVENTS); // Royal Specials
    MATCHES_TAB_DISP_NAME.put("MOTOR_SPEEDWAY", EVENTS);
    MATCHES_TAB_DISP_NAME.put("SQUASH", EVENTS);
    MATCHES_TAB_DISP_NAME.put("UFC", FIGHTS);
    MATCHES_TAB_DISP_NAME.put("WINTER_SPORTS", EVENTS);
    MATCHES_TAB_DISP_NAME.put("Chess", EVENTS); // Intentionally 'Chess'
    MATCHES_TAB_DISP_NAME.put("MOVIES", EVENTS);
    MATCHES_TAB_DISP_NAME.put("FORMULA_1", EVENTS);
  }

  @Override
  public boolean isValidForSport(SportCategory sportCategory) {
    return SportTier.TIER_2 == sportCategory.getTier();
  }

  @Override
  protected List<SportTab> getTabsBySport(String ssCategoryCode) {
    List<SportTab> tabs = new ArrayList<>();
    SportTab matchesTab = createMatchesTab(ssCategoryCode);
    tabs.add(matchesTab);
    if (ssCategoryCode.equals("GOLF")) tabs.addAll(TIER_2_GOLF_TABS);
    else tabs.addAll(TIER_2_TABS);
    return tabs;
  }

  private SportTab createMatchesTab(String sport) {
    String tabDisplayName = MATCHES_TAB_DISP_NAME.getOrDefault(sport, DEFAULT_MATCHES_DISP_NAME);
    return createTab(SportTabNames.MATCHES.nameLowerCase(), tabDisplayName, 1.0, true, true);
  }
}
