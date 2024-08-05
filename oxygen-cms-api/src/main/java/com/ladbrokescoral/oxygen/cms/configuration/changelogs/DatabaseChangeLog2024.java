package com.ladbrokescoral.oxygen.cms.configuration.changelogs;

import com.github.cloudyrock.mongock.ChangeLog;
import com.github.cloudyrock.mongock.ChangeSet;
import com.github.cloudyrock.mongock.driver.mongodb.springdata.v3.decorator.impl.MongockTemplate;
import com.ladbrokescoral.oxygen.cms.configuration.changelogs.script.SportModulesUpdate;

@ChangeLog(order = "003")
public class DatabaseChangeLog2024 {

  private static final String CORAL = "bma";
  private static final String LADBROKES = "ladbrokes";

  @ChangeSet(order = "01", id = "addPopularAccaModule", author = "system")
  public void addPopularAccaModule(MongockTemplate mongockTemplate) {
    new SportModulesUpdate().addPopularAccaModule(mongockTemplate, CORAL);
    new SportModulesUpdate().addPopularAccaModule(mongockTemplate, LADBROKES);
  }
}
