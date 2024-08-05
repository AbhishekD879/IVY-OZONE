package com.ladbrokescoral.oxygen.cms.configuration.changelogs.script;

import static com.ladbrokescoral.oxygen.cms.api.mapping.RacingModuleType.CORAL_LEGENDS;
import static com.ladbrokescoral.oxygen.cms.api.mapping.RacingModuleType.INTERNATIONAL_RACES;
import static com.ladbrokescoral.oxygen.cms.api.mapping.RacingModuleType.INTERNATIONAL_TOTE_CAROUSEL;
import static com.ladbrokescoral.oxygen.cms.api.mapping.RacingModuleType.LADBROKES_LEGENDS;
import static com.ladbrokescoral.oxygen.cms.api.mapping.RacingModuleType.UK_AND_IRISH_RACES;
import static com.ladbrokescoral.oxygen.cms.api.mapping.RacingModuleType.VIRTUAL_RACE_CAROUSEL;
import static com.ladbrokescoral.oxygen.cms.api.mapping.RacingModuleType.getRacingTypes;
import static java.util.stream.Collectors.toList;

import com.github.cloudyrock.mongock.driver.mongodb.springdata.v3.decorator.impl.MongockTemplate;
import com.ladbrokescoral.oxygen.cms.api.entity.Brand;
import com.ladbrokescoral.oxygen.cms.api.entity.InternationalToteConfig;
import com.ladbrokescoral.oxygen.cms.api.entity.PageType;
import com.ladbrokescoral.oxygen.cms.api.entity.RacingEventsModuleConfig;
import com.ladbrokescoral.oxygen.cms.api.entity.RacingModuleConfig;
import com.ladbrokescoral.oxygen.cms.api.entity.SportModule;
import com.ladbrokescoral.oxygen.cms.api.entity.SportModuleType;
import com.ladbrokescoral.oxygen.cms.api.entity.UkIrishRacingModuleConfig;
import com.ladbrokescoral.oxygen.cms.api.entity.VirtualRacingCarouselModuleConfig;
import com.ladbrokescoral.oxygen.cms.api.mapping.RacingModuleType;
import java.util.Arrays;
import java.util.Collections;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Objects;
import java.util.concurrent.atomic.AtomicInteger;
import lombok.extern.slf4j.Slf4j;
import org.springframework.core.env.Environment;
import org.springframework.data.mongodb.core.query.Criteria;
import org.springframework.data.mongodb.core.query.Query;
import org.springframework.data.mongodb.core.query.Update;
import org.springframework.util.ObjectUtils;
import org.springframework.util.StringUtils;

@Slf4j
public class RacingModuleUpdate extends AbstractBrandMongoUpdate {
  private static final Integer HORSE_RACING_ID = 21;
  private static final Integer GREYHOUNDS_ID = 19;
  private static final int HORSE_RACING_CLASS_ID = 285;
  private static final int GREYHOUND_CLASS_ID = 286;
  private static final String BRAND_SPORT_MODULE_PROPERTY = "brand";
  private static final String SPORT_ID_SPORT_MODULE_PROPERTY = "sportId";
  private static final String MODULE_TYPE_SPORT_MODULE_PROPERTY = "moduleType";
  private static final String TYPE_RACING_CONFIG_PROPERTY = "racingConfig.type";
  private static final String NAME_RACING_CONFIG_PROPERTY = "racingConfig.name";

  private static final Map<String, String> excludeTypesDefaults =
      new HashMap<String, String>() {
        {
          put("TST", "3048, 3049, 3123");
          put("STG", "16576, 16575, 16602");
          put("PRD", "28977, 28975, 29346");
        }
      };

  private static final Map<String, Map<Integer, Integer>> classIdsPerCategory =
      new HashMap<String, Map<Integer, Integer>>() {
        {
          Map<Integer, Integer> tstToteClasses = new HashMap<>();
          tstToteClasses.put(HORSE_RACING_ID, 16288);
          tstToteClasses.put(GREYHOUNDS_ID, 16290);
          put("TST", tstToteClasses);
          Map<Integer, Integer> stgToteClasses = new HashMap<>();
          stgToteClasses.put(HORSE_RACING_ID, 26512);
          stgToteClasses.put(GREYHOUNDS_ID, 26514);
          put("STG", stgToteClasses);
          Map<Integer, Integer> prdToteClasses = new HashMap<>();
          prdToteClasses.put(HORSE_RACING_ID, 802);
          prdToteClasses.put(GREYHOUNDS_ID, 804);
          put("PRD", prdToteClasses);
        }
      };

  private static final Map<Integer, Integer> virtualRacingClassIdDefaults =
      new HashMap<Integer, Integer>() {
        {
          put(HORSE_RACING_ID, HORSE_RACING_CLASS_ID);
          put(GREYHOUNDS_ID, GREYHOUND_CLASS_ID);
        }
      };

  private static final Map<Integer, Integer> eventSelectionDaysDefaults =
      new HashMap<Integer, Integer>() {
        {
          put(HORSE_RACING_ID, 6);
          put(GREYHOUNDS_ID, 2);
        }
      };

  private final MongockTemplate mongockTemplate;
  private Environment environment;

  public RacingModuleUpdate(MongockTemplate mongockTemplate) {
    this.mongockTemplate = mongockTemplate;
  }

  public RacingModuleUpdate(MongockTemplate mongockTemplate, Environment environment) {
    this.mongockTemplate = mongockTemplate;
    this.environment = environment;
  }

  public void addRacingModules(String brand) {
    addRacingModules(brand, HORSE_RACING_ID);
    addRacingModules(brand, GREYHOUNDS_ID);
  }

  public void updateInternationalToteModuleConfig(String brand) {
    updateDefaultRacingConfigs(
        brand,
        Arrays.asList(
            INTERNATIONAL_TOTE_CAROUSEL.getTitle(), INTERNATIONAL_TOTE_CAROUSEL.getAbbreviation()),
        new InternationalToteConfig());

    Arrays.asList(HORSE_RACING_ID, GREYHOUNDS_ID)
        .forEach(
            categoryId ->
                getAllRacingModules(brand, categoryId).stream()
                    .filter(
                        sportModule ->
                            sportModule
                                .getRacingConfig()
                                .getType()
                                .equals(INTERNATIONAL_TOTE_CAROUSEL))
                    .forEach(
                        sportModule ->
                            updateDefaultRacingConfigs(
                                brand,
                                Collections.singletonList(INTERNATIONAL_TOTE_CAROUSEL.toString()),
                                racingModuleSetDefaults(sportModule, getObEnv()),
                                false,
                                categoryId)));
  }

  public void updateVirtualRacingModuleDefaultConfigs(String obEnv, String brand) {
    updateDefaultRacingConfigs(
        brand,
        Arrays.asList(VIRTUAL_RACE_CAROUSEL.getTitle(), VIRTUAL_RACE_CAROUSEL.getAbbreviation()),
        new VirtualRacingCarouselModuleConfig());

    Arrays.asList(HORSE_RACING_ID, GREYHOUNDS_ID)
        .forEach(
            categoryId ->
                getAllRacingModules(brand, categoryId).stream()
                    .filter(sportModule -> Objects.nonNull(sportModule.getRacingConfig()))
                    .filter(
                        sportModule ->
                            VIRTUAL_RACE_CAROUSEL.equals(sportModule.getRacingConfig().getType()))
                    .forEach(
                        sportModule ->
                            updateDefaultRacingConfigs(
                                brand,
                                Collections.singletonList(VIRTUAL_RACE_CAROUSEL.toString()),
                                getVirtualRacingCarouselModuleConfig(categoryId, obEnv),
                                false,
                                categoryId)));
  }

  public void updateUkIrishRacingAndModulesDefaultConfigs(String brand) {
    updateDefaultRacingConfigs(
        brand,
        Arrays.asList(UK_AND_IRISH_RACES.getTitle(), UK_AND_IRISH_RACES.getAbbreviation()),
        getUKIrishRacingModuleConfig(HORSE_RACING_ID),
        true,
        HORSE_RACING_ID);
    updateDefaultRacingConfigs(
        brand,
        Arrays.asList(UK_AND_IRISH_RACES.getTitle(), UK_AND_IRISH_RACES.getAbbreviation()),
        getUKIrishRacingModuleConfig(GREYHOUNDS_ID),
        true,
        GREYHOUNDS_ID);

    getRacingTypes(brand).stream()
        .filter(t -> !UK_AND_IRISH_RACES.equals(t))
        .forEach(
            t ->
                updateDefaultRacingConfigs(
                    brand,
                    Arrays.asList(t.getTitle(), t.getAbbreviation()),
                    createDefaultConfig(t)));
  }

  private RacingModuleConfig createDefaultConfig(RacingModuleType type) {
    RacingModuleConfig config = new RacingModuleConfig();
    config.setType(type);
    return config;
  }

  public void updateRacingEventsModulesConfigs(String brand) {
    eventSelectionDaysDefaults
        .keySet()
        .forEach(
            (categoryId) -> {
              updateDefaultRacingConfigs(
                  brand,
                  Collections.singletonList(UK_AND_IRISH_RACES.toString()),
                  getUKIrishRacingModuleConfig(categoryId),
                  false,
                  categoryId);
              updateDefaultRacingConfigs(
                  brand,
                  Collections.singletonList(INTERNATIONAL_RACES.toString()),
                  getRacingEventModuleConfig(categoryId, INTERNATIONAL_RACES),
                  false,
                  categoryId);
              if (Brand.LADBROKES.equals(brand)) {
                updateDefaultRacingConfigs(
                    brand,
                    Collections.singletonList(LADBROKES_LEGENDS.toString()),
                    getRacingEventModuleConfig(categoryId, LADBROKES_LEGENDS),
                    false,
                    categoryId);
              } else if (Brand.BMA.equals(brand)) {
                updateDefaultRacingConfigs(
                    brand,
                    Collections.singletonList(CORAL_LEGENDS.toString()),
                    getRacingEventModuleConfig(categoryId, CORAL_LEGENDS),
                    false,
                    categoryId);
              }
            });
    updateDefaultRacingConfigs(
        brand,
        Arrays.asList(UK_AND_IRISH_RACES.getTitle(), UK_AND_IRISH_RACES.getAbbreviation()),
        new UkIrishRacingModuleConfig());

    getRacingTypes(brand).stream()
        .filter(t -> !UK_AND_IRISH_RACES.equals(t))
        .forEach(
            t ->
                updateDefaultRacingConfigs(
                    brand,
                    Arrays.asList(t.getTitle(), t.getAbbreviation()),
                    createDefaultConfig(t)));
  }

  public void deactivateGreyhoundsRacingModules(String brand) {
    Query configQuery =
        new Query()
            .addCriteria(
                Criteria.where(BRAND_SPORT_MODULE_PROPERTY)
                    .is(brand)
                    .and(SPORT_ID_SPORT_MODULE_PROPERTY)
                    .is(GREYHOUNDS_ID)
                    .and(MODULE_TYPE_SPORT_MODULE_PROPERTY)
                    .is(SportModuleType.RACING_MODULE.name())
                    .and(TYPE_RACING_CONFIG_PROPERTY)
                    .in(
                        INTERNATIONAL_TOTE_CAROUSEL,
                        VIRTUAL_RACE_CAROUSEL,
                        CORAL_LEGENDS,
                        LADBROKES_LEGENDS));

    mongockTemplate.updateMulti(
        configQuery, Update.update("disabled", true), SportModule.COLLECTION_NAME);
  }

  private void addRacingModules(String brand, Integer categoryId) {
    List<String> existingModulesNames =
        getAllRacingModules(brand, categoryId).stream()
            .map(SportModule::getRacingConfig)
            .map(RacingModuleConfig::getName)
            .collect(toList());

    AtomicInteger sortOrder = new AtomicInteger(100);
    getRacingTypes(brand).stream()
        .filter(type -> !existingModulesNames.contains(type.getTitle()))
        .forEach(type -> addRacingModule(type, brand, categoryId, sortOrder.getAndIncrement()));
  }

  private void addRacingModule(
      RacingModuleType type, String brand, Integer categoryId, int sortOrder) {
    SportModule module = new SportModule();
    RacingModuleConfig racingConfig = new RacingModuleConfig();
    racingConfig.setType(type);
    module.setRacingConfig(racingConfig);
    module.setTitle(type.getTitle());
    module.setBrand(brand);
    module.setDisabled(false);
    module.setSportId(categoryId);
    module.setPageType(PageType.sport);
    module.setModuleType(SportModuleType.RACING_MODULE);
    module.setSortOrder((double) sortOrder);

    mongockTemplate.insert(module, SportModule.COLLECTION_NAME);
  }

  private List<SportModule> getAllRacingModules(String brand, Integer categoryId) {
    Query query = new Query();
    query.addCriteria(
        Criteria.where(BRAND_SPORT_MODULE_PROPERTY)
            .is(brand)
            .and(SPORT_ID_SPORT_MODULE_PROPERTY)
            .is(categoryId)
            .and("pageType")
            .is(PageType.sport.name())
            .and(MODULE_TYPE_SPORT_MODULE_PROPERTY)
            .is(SportModuleType.RACING_MODULE.name()));
    return mongockTemplate.find(query, SportModule.class);
  }

  private void updateDefaultRacingConfigs(
      String brand, List<String> configNames, RacingModuleConfig defaultConfig) {
    updateDefaultRacingConfigs(brand, configNames, defaultConfig, true, null);
  }

  private void updateDefaultRacingConfigs(
      String brand,
      List<String> configNames,
      RacingModuleConfig defaultConfig,
      boolean useRacingConfigName,
      Integer categoryId) {
    Query configQuery =
        new Query()
            .addCriteria(
                Criteria.where(BRAND_SPORT_MODULE_PROPERTY)
                    .is(brand)
                    .and(MODULE_TYPE_SPORT_MODULE_PROPERTY)
                    .is(SportModuleType.RACING_MODULE.name()));

    configQuery.addCriteria(
        Criteria.where(
                useRacingConfigName ? NAME_RACING_CONFIG_PROPERTY : TYPE_RACING_CONFIG_PROPERTY)
            .in(configNames));

    if (!ObjectUtils.isEmpty(categoryId)) {
      configQuery.addCriteria(Criteria.where("pageId").is(categoryId.toString()));
    }

    mongockTemplate.updateMulti(
        configQuery, Update.update("racingConfig", defaultConfig), SportModule.COLLECTION_NAME);
  }

  private VirtualRacingCarouselModuleConfig getVirtualRacingCarouselModuleConfig(
      Integer sportId, String obEnv) {
    VirtualRacingCarouselModuleConfig currentConfig = new VirtualRacingCarouselModuleConfig();
    currentConfig.setExcludeTypeIds(excludeTypesDefaults.get(obEnv));
    if (currentConfig.getClassId() == 0) {
      currentConfig.setClassId(virtualRacingClassIdDefaults.getOrDefault(sportId, 0));
    }
    return currentConfig;
  }

  private UkIrishRacingModuleConfig getUKIrishRacingModuleConfig(Integer sportId) {
    UkIrishRacingModuleConfig config = new UkIrishRacingModuleConfig();
    // true for HorseRacing only
    config.setEnablePoolIndicators(HORSE_RACING_ID.equals(sportId));
    config.setEventsSelectionDays(eventSelectionDaysDefaults.getOrDefault(sportId, 0));
    return config;
  }

  private RacingEventsModuleConfig getRacingEventModuleConfig(
      Integer sportId, RacingModuleType moduleConfigType) {
    RacingEventsModuleConfig config = new RacingEventsModuleConfig();
    config.setType(moduleConfigType);
    config.setEventsSelectionDays(eventSelectionDaysDefaults.getOrDefault(sportId, 0));
    return config;
  }

  private RacingModuleConfig racingModuleSetDefaults(SportModule sportModule, String obEnv) {
    RacingModuleConfig racingModuleConfig = sportModule.getRacingConfig();

    if (racingModuleConfig.getType().equals(RacingModuleType.VIRTUAL_RACE_CAROUSEL)) {
      return getVirtualRacingCarouselModuleConfig(sportModule.getSportId(), obEnv);
    }

    if (racingModuleConfig.getType().equals(INTERNATIONAL_TOTE_CAROUSEL)) {
      InternationalToteConfig currentConfig = new InternationalToteConfig();
      currentConfig.setClassId(getClassIdByEnvAndSportId(obEnv, sportModule.getSportId()));
      return currentConfig;
    }

    return racingModuleConfig;
  }

  private int getClassIdByEnvAndSportId(String obEnv, int sportId) {
    return classIdsPerCategory.get(obEnv).get(sportId);
  }

  private String getObEnv() {
    String profiles =
        StringUtils.arrayToCommaDelimitedString(environment.getActiveProfiles()).toUpperCase();

    String env = "PRD";
    if (profiles.contains("DEV") || profiles.contains("TST") || profiles.contains("LOCAL")) {
      env = "TST";
    }

    if (profiles.contains("STG")) {
      env = "STG";
    }
    return env;
  }
}
