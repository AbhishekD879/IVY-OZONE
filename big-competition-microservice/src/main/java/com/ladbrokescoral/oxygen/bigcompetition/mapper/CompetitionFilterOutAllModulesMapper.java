package com.ladbrokescoral.oxygen.bigcompetition.mapper;

import com.ladbrokescoral.oxygen.cms.client.model.Competition;
import java.util.Collections;

public class CompetitionFilterOutAllModulesMapper {

  private CompetitionFilterOutAllModulesMapper() {}

  public static Competition filterOutAllModules(Competition competition) {
    competition
        .getCompetitionTabs()
        .forEach(
            tab -> {
              tab.setCompetitionModules(Collections.emptyList());
              tab.getCompetitionSubTabs()
                  .forEach(subTab -> subTab.setCompetitionModules(Collections.emptyList()));
            });
    return competition;
  }
}
