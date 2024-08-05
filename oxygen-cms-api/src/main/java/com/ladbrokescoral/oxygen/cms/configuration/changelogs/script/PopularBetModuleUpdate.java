package com.ladbrokescoral.oxygen.cms.configuration.changelogs.script;

import com.github.cloudyrock.mongock.driver.mongodb.springdata.v3.decorator.impl.MongockTemplate;
import com.ladbrokescoral.oxygen.cms.api.entity.PageType;
import com.ladbrokescoral.oxygen.cms.api.entity.PopularBetConfig;
import com.ladbrokescoral.oxygen.cms.api.entity.SportModule;
import com.ladbrokescoral.oxygen.cms.api.entity.SportModuleType;
import java.util.Collections;
import java.util.List;
import java.util.stream.Collectors;
import lombok.extern.slf4j.Slf4j;
import org.apache.commons.lang.WordUtils;
import org.springframework.data.mongodb.core.query.Criteria;
import org.springframework.data.mongodb.core.query.Query;

@Slf4j
public class PopularBetModuleUpdate extends AbstractBrandMongoUpdate {

  private static final int SPORT_ID = 0;

  private static final String BRAND_SPORT_MODULE_PROPERTY = "brand";

  private static final String SPORT_ID_SPORT_MODULE_PROPERTY = "sportId";

  private final MongockTemplate mongockTemplate;

  public PopularBetModuleUpdate(MongockTemplate mongockTemplate) {
    this.mongockTemplate = mongockTemplate;
  }

  public void addPopularBetModule(String brand) {
    addModule(brand, SPORT_ID);
  }

  public void addModule(String brand, Integer categoryId) {

    List<SportModuleType> list =
        getAllModules(brand, categoryId).stream()
            .map(SportModule::getModuleType)
            .collect(Collectors.toList());

    if (!list.contains(SportModuleType.POPULAR_BETS)) {
      createModule(brand, categoryId, list.size());
    }
  }

  public List<SportModule> getAllModules(String brand, Integer categoryId) {

    Query query = new Query();

    query.addCriteria(
        Criteria.where(BRAND_SPORT_MODULE_PROPERTY)
            .is(brand)
            .and(SPORT_ID_SPORT_MODULE_PROPERTY)
            .is(categoryId)
            .and("pageType")
            .is(PageType.sport.name()));

    return this.mongockTemplate.find(query, SportModule.class);
  }

  public void createModule(String brand, Integer categoryId, int sortOrder) {
    SportModule sportModule = new SportModule();
    sportModule.setTitle(getTitle(SportModuleType.POPULAR_BETS));
    sportModule.setBrand(brand);
    sportModule.setDisabled(false);
    sportModule.setSportId(categoryId);
    sportModule.setModuleType(SportModuleType.POPULAR_BETS);
    sportModule.setPageId(String.valueOf(categoryId));
    sportModule.setPageType(PageType.sport);
    sportModule.setSortOrder((double) sortOrder);
    sportModule.setPublishedDevices(Collections.emptyList());
    sportModule.setPopularBetConfig(createPopularBetConfig());

    this.mongockTemplate.insert(sportModule, SportModule.COLLECTION_NAME);
  }

  private PopularBetConfig createPopularBetConfig() {
    PopularBetConfig config = new PopularBetConfig();
    config.setPriceRange("10/19-20/21");
    config.setBackedInTimes("Backed in {n} Times!");
    return config;
  }

  private String getTitle(SportModuleType type) {
    return WordUtils.capitalizeFully(type.name().replace("_", " ")) + " Module";
  }
}
