package com.ladbrokescoral.oxygen.cms.api.service.sporttab;

import com.ladbrokescoral.oxygen.cms.api.entity.SportCategory;
import com.ladbrokescoral.oxygen.cms.api.entity.SportTab;
import com.ladbrokescoral.oxygen.cms.api.entity.SportTier;
import java.util.ArrayList;
import java.util.List;
import org.springframework.stereotype.Component;

@Component
public class Tier1SportTabsTemplate extends SportTabsTemplate {

  private static final List<SportTab> TIER_1_TABS = new ArrayList<>();

  // special tab configuration for football
  private static final List<SportTab> TIER_1_FOOTBALL_TABS = new ArrayList<>();
  public static final Double PB_SORTORDER = 8.0;

  static {
    TIER_1_TABS.add(createTab(SportTabNames.MATCHES.nameLowerCase(), "Matches", 1.0, false, true));
    TIER_1_TABS.add(createTab(SportTabNames.LIVE.nameLowerCase(), "In-Play", 2.0, false, true));
    TIER_1_TABS.add(
        createTab(SportTabNames.COMPETITIONS.nameLowerCase(), "Competitions", 3.0, false, true));
    TIER_1_TABS.add(createTab(SportTabNames.COUPONS.nameLowerCase(), "Coupons", 4.0, true, true));
    TIER_1_TABS.add(
        createTab(SportTabNames.OUTRIGHTS.nameLowerCase(), "Outrights", 5.0, false, true));
    TIER_1_TABS.add(createTab(SportTabNames.SPECIALS.nameLowerCase(), "Specials", 7.0, true, true));

    TIER_1_FOOTBALL_TABS.addAll(TIER_1_TABS);
    TIER_1_FOOTBALL_TABS.add(
        createTab(SportTabNames.JACKPOT.nameLowerCase(), "Jackpot", 6.0, true, true));
    TIER_1_FOOTBALL_TABS.add(
        createTab(
            SportTabNames.POPULARBETS.nameLowerCase(), "Popular Bets", PB_SORTORDER, false, true));
  }

  @Override
  public boolean isValidForSport(SportCategory sportCategory) {
    return SportTier.TIER_1 == sportCategory.getTier();
  }

  @Override
  public List<SportTab> getTabsBySport(String ssCategoryCode) {
    if ("FOOTBALL".equals(ssCategoryCode)) {
      return TIER_1_FOOTBALL_TABS;
    }
    return TIER_1_TABS;
  }
}
