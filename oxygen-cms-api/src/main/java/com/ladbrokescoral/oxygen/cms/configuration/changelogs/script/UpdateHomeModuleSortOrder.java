package com.ladbrokescoral.oxygen.cms.configuration.changelogs.script;

import com.github.cloudyrock.mongock.driver.mongodb.springdata.v3.decorator.impl.MongockTemplate;
import com.ladbrokescoral.oxygen.cms.api.entity.HomeModule;
import java.util.List;
import lombok.extern.slf4j.Slf4j;
import org.apache.commons.lang3.ObjectUtils;

@Slf4j
public class UpdateHomeModuleSortOrder {

  private static final String HOMEMODULES_COLLECTION_NAME = "homemodules";

  public void updateSortOrder(MongockTemplate mongockTemplate) {

    List<HomeModule> homeModules =
        mongockTemplate.findAll(HomeModule.class, HOMEMODULES_COLLECTION_NAME);

    homeModules.forEach(
        (HomeModule homeModule) -> {
          if (ObjectUtils.isEmpty(homeModule.getSortOrder())) {
            homeModule.setSortOrder(homeModule.getDisplayOrder());
            mongockTemplate.save(homeModule);
          }
        });
  }
}
