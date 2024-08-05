package com.ladbrokescoral.oxygen.cms.api.service.sporttab;

import com.ladbrokescoral.oxygen.cms.api.entity.SportCategory;
import com.ladbrokescoral.oxygen.cms.api.entity.SportTab;
import com.ladbrokescoral.oxygen.cms.api.entity.SportTier;
import java.util.ArrayList;
import java.util.List;
import org.springframework.stereotype.Component;

@Component
public class UntiedSportTabsTemplate extends SportTabsTemplate {
  private static final List<SportTab> UNTIED_SPORT_TABS_GREYHOUNDS = new ArrayList<>();
  private static final List<SportTab> UNTIED_SPORT_TABS_HORSERACING = new ArrayList<>();
  private static final double UNTIED_SPORT_GH_TODAY_SORT_ORDER = 1.0;
  private static final double UNTIED_SPORT_GH_TOMORROW_SORT_ORDER = 2.0;
  private static final double UNTIED_SPORT_HR_MEETINGS_SORT_ORDER = 3.0;

  static {
    UNTIED_SPORT_TABS_GREYHOUNDS.add(
        createTab(
            SportTabNames.TODAY.nameLowerCase(),
            "Today",
            UNTIED_SPORT_GH_TODAY_SORT_ORDER,
            false,
            true));
    UNTIED_SPORT_TABS_GREYHOUNDS.add(
        createTab(
            SportTabNames.TOMORROW.nameLowerCase(),
            "Tomorrow",
            UNTIED_SPORT_GH_TOMORROW_SORT_ORDER,
            false,
            true));
    UNTIED_SPORT_TABS_HORSERACING.add(
        createTab(
            SportTabNames.MEETINGS.nameLowerCase(),
            "Meetings",
            UNTIED_SPORT_HR_MEETINGS_SORT_ORDER,
            false,
            true));
  }

  @Override
  public boolean isValidForSport(SportCategory sportCategory) {
    return SportTier.UNTIED == sportCategory.getTier();
  }

  @Override
  protected List<SportTab> getTabsBySport(String ssCategoryCode) {

    List<SportTab> tabs = new ArrayList<>();
    if (ssCategoryCode.equals("GREYHOUNDS")) tabs.addAll(UNTIED_SPORT_TABS_GREYHOUNDS);
    else if (ssCategoryCode.equals("HORSERACING")) tabs.addAll(UNTIED_SPORT_TABS_HORSERACING);
    return tabs;
  }
}
