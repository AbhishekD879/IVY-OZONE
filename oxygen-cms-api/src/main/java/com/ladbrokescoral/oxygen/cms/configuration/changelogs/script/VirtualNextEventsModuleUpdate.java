package com.ladbrokescoral.oxygen.cms.configuration.changelogs.script;

import com.github.cloudyrock.mongock.driver.mongodb.springdata.v3.decorator.impl.MongockTemplate;
import com.ladbrokescoral.oxygen.cms.api.entity.PageType;
import com.ladbrokescoral.oxygen.cms.api.entity.SportModule;
import com.ladbrokescoral.oxygen.cms.api.entity.SportModuleType;
import java.util.Collections;
import java.util.List;
import java.util.stream.Collectors;
import lombok.extern.slf4j.Slf4j;
import org.apache.commons.lang3.text.WordUtils;
import org.springframework.data.mongodb.core.query.Criteria;
import org.springframework.data.mongodb.core.query.Query;

@Slf4j
public class VirtualNextEventsModuleUpdate extends AbstractBrandMongoUpdate {

  private static final int VIRTUALS_SPORT_ID = 39;

  private static final String BRAND_SPORT_MODULE_PROPERTY = "brand";

  private static final String SPORT_ID_SPORT_MODULE_PROPERTY = "sportId";

  private static final String PAGE_TYPE = "pageType";

  private static final String MODULE_TYPE = "moduleType";

  private final MongockTemplate mongockTemplate;

  public VirtualNextEventsModuleUpdate(MongockTemplate mongockTemplate) {
    this.mongockTemplate = mongockTemplate;
  }

  public void addVirtualNextEventsModule(String brand) {
    addModule(brand, VIRTUALS_SPORT_ID);
  }

  public void addModule(String brand, Integer categoryId) {

    List<SportModuleType> list =
        getAllVirtualsModules(brand, categoryId).stream()
            .map(SportModule::getModuleType)
            .collect(Collectors.toList());

    if (!list.contains(SportModuleType.VIRTUAL_NEXT_EVENTS)) {
      createModule(brand, categoryId, list.size());
    }
  }

  public List<SportModule> getAllVirtualsModules(String brand, Integer categoryId) {

    Query query = new Query();

    query.addCriteria(
        Criteria.where(BRAND_SPORT_MODULE_PROPERTY)
            .is(brand)
            .and(SPORT_ID_SPORT_MODULE_PROPERTY)
            .is(categoryId)
            .and(PAGE_TYPE)
            .is(PageType.sport.name()));

    return this.mongockTemplate.find(query, SportModule.class);
  }

  public void createModule(String brand, Integer categoryId, int sortOrder) {
    SportModule sportModule = new SportModule();
    sportModule.setTitle(getTitle(SportModuleType.VIRTUAL_NEXT_EVENTS));
    sportModule.setBrand(brand);
    sportModule.setDisabled(false);
    sportModule.setSportId(categoryId);
    sportModule.setModuleType(SportModuleType.VIRTUAL_NEXT_EVENTS);
    sportModule.setPageId(String.valueOf(categoryId));
    sportModule.setPageType(PageType.sport);
    sportModule.setSortOrder((double) sortOrder);
    sportModule.setPublishedDevices(Collections.emptyList());
    this.mongockTemplate.insert(sportModule, SportModule.COLLECTION_NAME);
  }

  private String getTitle(SportModuleType type) {
    return WordUtils.capitalizeFully(type.name().replace("_", " ")) + " Module";
  }
}
