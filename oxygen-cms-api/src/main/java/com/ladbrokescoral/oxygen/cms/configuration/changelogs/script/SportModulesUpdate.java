package com.ladbrokescoral.oxygen.cms.configuration.changelogs.script;

import static java.util.Collections.emptyList;

import com.github.cloudyrock.mongock.driver.mongodb.springdata.v3.decorator.impl.MongockTemplate;
import com.ladbrokescoral.oxygen.cms.api.entity.*;
import java.time.Instant;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.function.Function;
import java.util.stream.Collectors;
import java.util.stream.Stream;
import lombok.extern.slf4j.Slf4j;
import org.apache.commons.collections4.CollectionUtils;
import org.apache.commons.lang3.text.WordUtils;

@Slf4j
public class SportModulesUpdate extends AbstractBrandMongoUpdate {

  private static final String SPORT_CATEGORIES_COLLECTION_NAME = "sportcategories";
  private static final String SPORT_MODULES_COLLECTION_NAME = "sportmodules";

  private static final int FOOTBALL = 16;

  private static final int SORT_ORDER = -200;

  private static final int POPULAR_ACCA_SORT_ORDER = -201;

  private static final String POPULAR_ACCA_TITLE = "Popular Acca Widget";

  public void initSportModules(MongockTemplate mongockTemplate, String brand) {
    try {
      List<SportModule> existingSportModules =
          findAllByBrand(mongockTemplate, brand, SPORT_MODULES_COLLECTION_NAME, SportModule.class);
      Map<Integer, List<SportModule>> existingModulesPerPage = groupByPageId(existingSportModules);

      List<SportModule> newModules =
          getSportPagesIdsStream(mongockTemplate, brand)
              .distinct()
              .flatMap(
                  categoryId ->
                      initSportModules(
                          brand,
                          categoryId,
                          existingModulesPerPage.getOrDefault(categoryId, emptyList()))
                          .stream())
              .collect(Collectors.toList());
      mongockTemplate.insert(newModules, SPORT_MODULES_COLLECTION_NAME);

    } catch (Exception e) {
      log.error("Failed to initSportModules for {} brand", brand, e);
      throw e;
    }
  }

  public void addUngroupedFeaturedSportsModuleForHomepage(
      MongockTemplate mongockTemplate, String brand) {
    SportModule sportModule =
        createModule(brand, SportModuleType.UNGROUPED_FEATURED, 0, "0", PageType.sport, -180);
    sportModule.setDisabled(false);
    sportModule.setTitle("Ungrouped featured events");
    mongockTemplate.insert(sportModule, SPORT_MODULES_COLLECTION_NAME);
  }

  private Stream<Integer> getSportPagesIdsStream(MongockTemplate mongockTemplate, String brand) {
    return Stream.concat(
        Stream.of(0), // adding homePage
        findAllByBrand(
                mongockTemplate, brand, SPORT_CATEGORIES_COLLECTION_NAME, SportCategory.class)
            .stream()
            .map(SportCategory::getCategoryId));
  }

  private Map<Integer, List<SportModule>> groupByPageId(List<SportModule> existingSportModules) {
    return existingSportModules.stream()
        .filter(m -> PageType.sport.equals(m.getPageType()))
        .collect(Collectors.groupingBy(m -> Integer.valueOf(m.getPageId())));
  }

  private List<SportModule> initSportModules(
      String brand, Integer sportCategoryId, List<SportModule> existingModules) {
    Set<SportModuleType> existingTypes =
        existingModules.stream().map(SportModule::getModuleType).collect(Collectors.toSet());
    int nextSortOrder = existingTypes.size();

    List<SportModule> newModules = new ArrayList<>(SportModuleType.values().length);
    for (SportModuleType type : SportModuleType.values()) {
      if (!existingTypes.contains(type)) {
        newModules.add(
            createModule(
                brand,
                type,
                sportCategoryId,
                String.valueOf(sportCategoryId),
                PageType.sport,
                nextSortOrder++));
      }
    }
    return newModules;
  }

  public void createAemBanners(MongockTemplate mongockTemplate, String brand) {
    try {
      List<SportModule> existingSportModules =
          findAllByBrand(mongockTemplate, brand, SPORT_MODULES_COLLECTION_NAME, SportModule.class);
      Function<SportModule, String> sportModuleStringFunction =
          m -> String.format("%s%s", m.getPageId(), m.getPageType());
      Set<SportModule> noBannerPages =
          existingSportModules.stream()
              .filter(m -> !PageType.edp.equals(m.getPageType()))
              .collect(Collectors.groupingBy(sportModuleStringFunction))
              .values()
              .stream()
              .filter(
                  sportModules ->
                      sportModules.stream()
                          .noneMatch(sm -> SportModuleType.AEM_BANNERS.equals(sm.getModuleType())))
              .map(sportModules -> sportModules.get(0))
              .collect(Collectors.toSet());

      final Set<SportModule> newModules = new HashSet<>();
      noBannerPages.forEach(
          someModule -> {
            newModules.add(createAemBannerModule(brand, someModule, 1));
            newModules.add(createAemBannerModule(brand, someModule, 2));
            newModules.add(createAemBannerModule(brand, someModule, 3));
            newModules.add(createAemBannerModule(brand, someModule, 4));
          });

      mongockTemplate.insert(newModules, SPORT_MODULES_COLLECTION_NAME);

    } catch (Exception e) {
      log.error("Failed to initSportModules for {} brand", brand, e);
      throw e;
    }
  }

  private SportModule createAemBannerModule(String brand, SportModule similarModule, int index) {
    SportModule module = new SportModule();
    module.setBrand(brand);
    module.setModuleType(SportModuleType.AEM_BANNERS);
    module.setPageId(similarModule.getPageId());
    module.setPageType(similarModule.getPageType());
    module.setDisabled(true);
    module.setPublishedDevices(emptyList());
    module.setSportId(similarModule.getSportId());
    module.setTitle("AEM banners carousel #" + index);
    module.setSortOrder((double) index);
    module.setModuleConfig(
        AemBannersConfig.builder()
            .maxOffers(7)
            .timePerSlide(7)
            .displayFrom(Instant.now())
            .displayTo(Instant.now().plusSeconds(10))
            .build());
    return module;
  }

  private SportModule createModule(
      String brand,
      SportModuleType moduleType,
      Integer sportId,
      String pageId,
      PageType pageType,
      int sortOrder) {
    SportModule module = new SportModule();
    module.setBrand(brand);
    module.setModuleType(moduleType);
    module.setPageId(pageId);
    module.setPageType(pageType);
    module.setDisabled(true);
    module.setPublishedDevices(emptyList());
    module.setSportId(sportId);
    module.setTitle(getTitle(moduleType));
    module.setSortOrder((double) sortOrder);
    if (SportModuleType.INPLAY.equals(moduleType)) {
      module.setInplayConfig(new HomeInplayConfig());
    } else if (SportModuleType.RECENTLY_PLAYED_GAMES.equals(moduleType)) {
      module.setRpgConfig(new RpgConfig());
    }
    return module;
  }

  private String getTitle(SportModuleType type) {
    return WordUtils.capitalizeFully(type.name().replace("_", " ")) + " Module";
  }

  public void addBybWidgetModule(MongockTemplate mongockTemplate, String brand) {

    createModule(brand, SportModuleType.BYB_WIDGET, 0, "BYB Widget Module", mongockTemplate);
    createModule(brand, SportModuleType.BYB_WIDGET, FOOTBALL, "BYB Widget Module", mongockTemplate);
  }

  public void addSuperButtonModule(MongockTemplate mongockTemplate, String brand) {

    createModule(brand, SportModuleType.SUPER_BUTTON, 0, "SUPER Button Module", mongockTemplate);
  }

  private void createModule(
      String brand,
      SportModuleType moduleType,
      int sportId,
      String moduleTitle,
      MongockTemplate mongockTemplate) {
    SportModule sportModule =
        createModule(
            brand, moduleType, sportId, String.valueOf(sportId), PageType.sport, SORT_ORDER);
    sportModule.setDisabled(true);
    sportModule.setTitle(moduleTitle);
    mongockTemplate.insert(sportModule, SPORT_MODULES_COLLECTION_NAME);
  }

  public void addLuckyDipSportModule(MongockTemplate mongockTemplate, String brand) {

    initLuckyDipSportModule(
        brand, SportModuleType.LUCKY_DIP, 0, "LuckyDip Module", mongockTemplate);
  }

  public void initLuckyDipSportModule(
      String brand,
      SportModuleType luckyDip,
      int sportId,
      String luckyDipTitle,
      MongockTemplate mongockTemplate) {
    try {
      List<SportModule> existingSportModules =
          findAllByBrand(mongockTemplate, brand, SPORT_MODULES_COLLECTION_NAME, SportModule.class);
      Map<Integer, List<SportModule>> existingModulesPerPage = groupByPageId(existingSportModules);
      List<SportModule> homePageModules = existingModulesPerPage.get(sportId);

      SportModule module;
      if (CollectionUtils.isNotEmpty(homePageModules)
          && homePageModules.stream()
              .noneMatch(sportModule -> luckyDip.equals(sportModule.getModuleType()))) {
        int nextSortOrder = homePageModules.size();
        module = new SportModule();
        module.setBrand(brand);
        module.setModuleType(luckyDip);
        module.setPageId(String.valueOf(sportId));
        module.setPageType(PageType.sport);
        module.setDisabled(true);
        module.setSportId(sportId);
        module.setTitle(luckyDipTitle);
        module.setSortOrder((double) nextSortOrder);
        mongockTemplate.insert(module, SPORT_MODULES_COLLECTION_NAME);
      }

    } catch (Exception e) {
      log.error("Failed to initSportModules for {} luckyDip", brand, e);
      throw e;
    }
  }

  public void addPopularAccaModule(MongockTemplate mongockTemplate, String brand) {
    createModule(
        mongockTemplate,
        brand,
        SportModuleType.POPULAR_ACCA,
        0,
        POPULAR_ACCA_TITLE,
        POPULAR_ACCA_SORT_ORDER);
    createModule(
        mongockTemplate,
        brand,
        SportModuleType.POPULAR_ACCA,
        FOOTBALL,
        POPULAR_ACCA_TITLE,
        POPULAR_ACCA_SORT_ORDER);
  }

  private void createModule(
      MongockTemplate mongockTemplate,
      String brand,
      SportModuleType moduleType,
      Integer sportId,
      String moduleTitle,
      int sortOrder) {
    SportModule sportModule =
        createModule(
            brand, moduleType, sportId, String.valueOf(sportId), PageType.sport, sortOrder);
    sportModule.setDisabled(true);
    sportModule.setTitle(moduleTitle);
    mongockTemplate.insert(sportModule, SPORT_MODULES_COLLECTION_NAME);
  }
}
