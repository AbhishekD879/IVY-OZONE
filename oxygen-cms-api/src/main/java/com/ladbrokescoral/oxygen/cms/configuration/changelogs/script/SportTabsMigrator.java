package com.ladbrokescoral.oxygen.cms.configuration.changelogs.script;

import static java.util.stream.Collectors.groupingBy;
import static java.util.stream.Collectors.toMap;

import com.github.cloudyrock.mongock.driver.mongodb.springdata.v3.decorator.impl.MongockTemplate;
import com.ladbrokescoral.oxygen.cms.api.entity.*;
import com.ladbrokescoral.oxygen.cms.api.service.sporttab.*;
import java.util.*;
import java.util.function.Function;
import java.util.stream.Collectors;
import java.util.stream.Stream;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.mongodb.core.query.Criteria;
import org.springframework.data.mongodb.core.query.Query;
import org.springframework.data.mongodb.core.query.Update;

@Slf4j
public class SportTabsMigrator extends AbstractBrandMongoUpdate {
  private static final String SPORT_TABS_COLLECTION_NAME = "sporttabs";
  private MongockTemplate mongockTemplate;
  private final List<SportTabsTemplate> tabsTemplates;
  private static final double TIER_DIGIT_7_0 = 7.0;
  private static final double TIER_DIGIT_5_0 = 5.0;

  public SportTabsMigrator(MongockTemplate mongockTemplate) {
    this.mongockTemplate = mongockTemplate;
    this.tabsTemplates =
        Arrays.asList(
            new Tier1SportTabsTemplate(),
            new Tier2SportTabsTemplate(),
            new UntiedSportTabsTemplate());
  }

  public void updateCheckEventsForTier1SportsTab(String brand) {
    Stream.of(MainTier1Sports.values())
        .forEach(
            (MainTier1Sports category) -> {
              SportCategory sportCategory = createSportCategoryMock(category, brand);
              new Tier1SportTabsTemplate()
                  .getTabsBySport(sportCategory.getSsCategoryCode())
                  .forEach(
                      tab ->
                          mongockTemplate.updateMulti(
                              getFindByBrandQuery(brand)
                                  .addCriteria(
                                      Criteria.where("sportId").is(sportCategory.getCategoryId()))
                                  .addCriteria(Criteria.where("name").is(tab.getName())),
                              Update.update("checkEvents", tab.isCheckEvents())
                                  .set("sortOrder", tab.getSortOrder()),
                              SportTab.class,
                              SPORT_TABS_COLLECTION_NAME));
            });
  }

  private SportCategory createSportCategoryMock(MainTier1Sports category, String brand) {
    SportCategory sportCategory = new SportCategory();
    sportCategory.setBrand(brand);
    sportCategory.setCategoryId(category.getCategoryId());
    sportCategory.setSsCategoryCode(category.name());
    return sportCategory;
  }

  private List<SportTab> getDefaultTabs(SportCategory sportCategory) {
    return tabsTemplates.stream()
        .filter(template -> template.isValidForSport(sportCategory))
        .findFirst()
        .orElseThrow(IllegalArgumentException::new)
        .buildTabs(sportCategory);
  }

  public void updateSportsTabsAccordingToTemplates(String brand) {
    Map<Integer, Map<String, SportTab>> sportsTabsByName =
        findAllByBrand(mongockTemplate, brand, SportTab.class).stream()
            .collect(
                groupingBy(SportTab::getSportId, toMap(SportTab::getName, Function.identity())));
    findAllByBrand(mongockTemplate, brand, SportCategory.class)
        .forEach(
            (SportCategory category) -> {
              Map<String, SportTab> existingTabsByName =
                  sportsTabsByName.getOrDefault(category.getCategoryId(), new HashMap<>());
              Map<String, SportTab> defaultTabsByName =
                  getDefaultTabs(category).stream()
                      .collect(toMap(SportTab::getName, Function.identity()));
              existingTabsByName.values().stream() // remove tabs that are out from template
                  .filter(existingTab -> !defaultTabsByName.containsKey(existingTab.getName()))
                  .forEach(existingTab -> mongockTemplate.remove(existingTab));
              defaultTabsByName
                  .values()
                  .forEach(
                      defaultTab ->
                          mongockTemplate.save(adjustSportTab(existingTabsByName, defaultTab)));
            });
  }

  public void addSpecialsTabForTier1n2SportsTab(String brand) {
    List<Integer> categoriesWithSpecials =
        findAllByBrand(mongockTemplate, brand, SportTab.class).stream()
            .filter(
                sportTab ->
                    SportTabNames.SPECIALS
                        .nameLowerCase()
                        .equals(sportTab.getName().toLowerCase(Locale.ENGLISH)))
            .mapToInt(SportTab::getSportId)
            .boxed()
            .collect(Collectors.toList());
    findAllByBrand(mongockTemplate, brand, SportCategory.class).stream()
        .filter(
            (SportCategory sportCategory) ->
                MainTier1Sports.FOOTBALL.getCategoryId() != sportCategory.getCategoryId())
        .filter(
            sportCategory ->
                SportTier.TIER_1.equals(sportCategory.getTier())
                    || SportTier.TIER_2.equals(sportCategory.getTier()))
        .filter(sportCategory -> !categoriesWithSpecials.contains(sportCategory.getCategoryId()))
        .forEach(
            (SportCategory sportCategory) -> {
              SportTab tab =
                  SportTabsTemplate.createTab(
                      SportTabNames.SPECIALS.nameLowerCase(),
                      "Specials",
                      SportTier.TIER_1.equals(sportCategory.getTier())
                          ? TIER_DIGIT_7_0
                          : TIER_DIGIT_5_0,
                      true,
                      true);
              tab.setBrand(brand);
              tab.setSportId(sportCategory.getCategoryId());
              mongockTemplate.save(tab, SPORT_TABS_COLLECTION_NAME);
            });
  }

  private SportTab adjustSportTab(Map<String, SportTab> existingTabsByName, SportTab defaultTab) {
    SportTab existingTab = existingTabsByName.get(defaultTab.getName());
    if (Objects.nonNull(existingTab)) {
      existingTab.setSortOrder(defaultTab.getSortOrder());
      existingTab.setCheckEvents(defaultTab.isCheckEvents());
      if (!defaultTab.isEnabled()) {
        existingTab.setEnabled(false);
      }
      return existingTab;
    }
    return defaultTab;
  }

  public void removeDuplicateTabs(String brand) {
    List<SportTab> sportTabs =
        findAllByBrand(mongockTemplate, brand, SPORT_TABS_COLLECTION_NAME, SportTab.class);
    Map<Integer, Map<String, List<SportTab>>> groupedBySportAndName =
        sportTabs.stream().collect(groupingBy(SportTab::getSportId, groupingBy(SportTab::getName)));

    List<String> extraTabs =
        groupedBySportAndName.values().stream()
            .flatMap(map -> map.entrySet().stream())
            .filter(e -> e.getValue().size() > 1)
            .flatMap(e -> getOlderSportTabs(e.getValue()))
            .map(AbstractEntity::getId)
            .collect(Collectors.toList());
    if (extraTabs.isEmpty()) {
      return;
    }

    long removed =
        mongockTemplate
            .remove(Query.query(Criteria.where("_id").in(extraTabs)), SPORT_TABS_COLLECTION_NAME)
            .getDeletedCount();
    log.info("Removing {} extra tabs for brand {}", removed, brand);
  }

  private Stream<SportTab> getOlderSportTabs(List<SportTab> duplicatedSportTabs) {
    return duplicatedSportTabs.stream()
        .sorted(Comparator.comparing(AbstractEntity::getCreatedAt))
        .limit(duplicatedSportTabs.size() - 1L);
  }

  public void addTabsForInplayGolf(MongockTemplate mongockTemplate, String brand) {

    SportCategory sportCategory = createSportCategoryMockForTier2(MainTier2Sports.GOLF, brand);
    new Tier2SportTabsTemplate()
        .buildTabs(sportCategory)
        .forEach(
            (SportTab tab) -> {
              if (tab.getName().equals("live")) {
                mongockTemplate.save(tab, SPORT_TABS_COLLECTION_NAME);
              }
            });
  }

  private SportCategory createSportCategoryMockForTier2(MainTier2Sports category, String brand) {
    SportCategory sportCategory = new SportCategory();
    sportCategory.setBrand(brand);
    sportCategory.setCategoryId(category.getCategoryId());
    sportCategory.setSsCategoryCode(category.name());
    return sportCategory;
  }

  public void addTabsForGolf(MongockTemplate mongockTemplate, String brand) {

    SportCategory sportCategory = createSportCategoryMockForTier2(MainTier2Sports.GOLF, brand);
    new Tier2SportTabsTemplate()
        .buildTabs(sportCategory)
        .forEach(
            (SportTab tab) -> {
              if (tab.getName().equals("golf_matches")) {
                mongockTemplate.save(tab, SPORT_TABS_COLLECTION_NAME);
              }
            });
  }

  public void addTabsForAnySportTier(SportTabMetaData sportTabMetaData) {
    SportCategory sportCategory =
        createSportCategoryMockForSport(
            sportTabMetaData.getAllSports(),
            sportTabMetaData.getBrand(),
            sportTabMetaData.getAllSports().getCategoryId());
    sportTabMetaData
        .getSportTabsTemplate()
        .buildTabs(sportCategory)
        .forEach(
            (SportTab tab) -> {
              if (tab.getName().equals(sportTabMetaData.getTabName().toLowerCase())) {
                mongockTemplate.save(tab, SPORT_TABS_COLLECTION_NAME);
              }
            });
  }

  private SportCategory createSportCategoryMockForSport(
      AllSports category, String brand, int categoryId) {
    SportCategory sportCategory = new SportCategory();
    sportCategory.setBrand(brand);
    sportCategory.setCategoryId(categoryId);
    sportCategory.setSsCategoryCode(category.getName());
    return sportCategory;
  }

  public void addOrUpdateTrendingTabsForSportTab(
      String brand,
      int sportId,
      String tabName,
      String trendingTab,
      String headerDisplayName,
      List<String> popularTabs) {
    Query query =
        getFindByBrandQuery(brand)
            .addCriteria(Criteria.where("sportId").is(sportId))
            .addCriteria(Criteria.where("name").is(tabName));
    SportTab sportTab = mongockTemplate.findOne(query, SportTab.class);
    Optional.ofNullable(sportTab)
        .ifPresent(
            (SportTab st) -> {
              if (st.getTrendingTabs() == null) {
                st.setTrendingTabs(new ArrayList<>());
              }
              st.getTrendingTabs()
                  .add(
                      prepareTrendingTab(
                          brand, sportId, trendingTab, headerDisplayName, popularTabs));
              mongockTemplate.save(sportTab);
            });
  }

  private TrendingTab prepareTrendingTab(
      String brand,
      int sportId,
      String trendingTab,
      String headerDisplayName,
      List<String> popularTabs) {
    List<PopularTab> popularTabsEntities = new ArrayList<>();
    popularTabs.forEach(
        (String popularTabName) -> {
          PopularTab tab = new PopularTab();
          tab.setBrand(brand);
          tab.setSportId(sportId);
          tab.setHref(popularTabName);
          tab.setPopularTabName(popularTabName);
          tab.setHeaderDisplayName(popularTabName);
          popularTabsEntities.add(mongockTemplate.save(tab));
        });
    TrendingTab trendingTabEntity = new TrendingTab();
    trendingTabEntity.setBrand(brand);
    trendingTabEntity.setSportId(sportId);
    trendingTabEntity.setHref(trendingTab);
    trendingTabEntity.setTrendingTabName(trendingTab);
    trendingTabEntity.setHeaderDisplayName(headerDisplayName);
    trendingTabEntity.setPopularTabs(popularTabsEntities);
    return mongockTemplate.save(trendingTabEntity);
  }
}
