package com.ladbrokescoral.oxygen.cms.configuration.changelogs.script;

import com.github.cloudyrock.mongock.driver.mongodb.springdata.v3.decorator.impl.MongockTemplate;
import com.ladbrokescoral.oxygen.cms.api.entity.PageType;
import com.ladbrokescoral.oxygen.cms.api.entity.SportModule;
import com.ladbrokescoral.oxygen.cms.api.entity.SportModuleType;
import com.ladbrokescoral.oxygen.cms.api.entity.TeamAndFansBetsConfig;
import java.util.Collections;
import lombok.extern.slf4j.Slf4j;
import org.apache.commons.lang3.StringUtils;

@Slf4j
public class TeamAndFansBetsModuleUpdate extends AbstractBrandMongoUpdate {
  private static final int FANZONE_SPORT_ID = 160;
  private static final String BRAND = "ladbrokes";

  public void createBetsModulesForFanzone(
      MongockTemplate mongockTemplate, SportModuleType moduleType) {
    SportModule sportModule = createBetsBasedOnTeamAndFansModule(moduleType, FANZONE_SPORT_ID, 0);
    mongockTemplate.insert(sportModule, SportModule.COLLECTION_NAME);
  }

  private SportModule createBetsBasedOnTeamAndFansModule(
      SportModuleType moduleType, Integer sportId, int sortOrder) {

    SportModule sportModule = new SportModule();
    sportModule.setBrand(BRAND);
    sportModule.setDisabled(true);
    sportModule.setSportId(sportId);
    sportModule.setPageId(String.valueOf(sportId));
    sportModule.setPageType(PageType.sport);
    sportModule.setSortOrder((double) sortOrder);
    sportModule.setPublishedDevices(Collections.emptyList());
    sportModule.setTitle(getTitle(moduleType));
    sportModule.setModuleType(moduleType);
    sportModule.setTeamAndFansBetsConfig(new TeamAndFansBetsConfig());
    return sportModule;
  }

  private String getTitle(SportModuleType type) {
    return StringUtils.capitalize(type.name().replace("_", " "));
  }
}
