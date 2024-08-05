package com.ladbrokescoral.oxygen.cms.api.service.sporttab;

import com.ladbrokescoral.oxygen.cms.api.entity.PopularTab;
import com.ladbrokescoral.oxygen.cms.api.entity.SportCategory;
import com.ladbrokescoral.oxygen.cms.api.entity.SportTab;
import com.ladbrokescoral.oxygen.cms.api.entity.TrendingTab;
import com.ladbrokescoral.oxygen.cms.api.repository.PopularTabRepository;
import com.ladbrokescoral.oxygen.cms.api.repository.SportTabRepository;
import com.ladbrokescoral.oxygen.cms.api.repository.TrendingTabRepository;
import com.ladbrokescoral.oxygen.cms.api.service.SortableService;
import java.util.Collections;
import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

@Service
@Slf4j
public class SportTabService extends SortableService<SportTab> {

  private final SportTabRepository sportTabRepository;

  private final TrendingTabRepository trendingTabRepository;

  private final PopularTabRepository popularTabRepository;

  private final List<SportTabsTemplate> templates;

  private static final List<String> TABS_WITHOUT_CHECK_EVENTS_FUNCTIONALITY =
      Collections.singletonList(SportTabNames.LIVE.nameLowerCase());

  public SportTabService(
      SportTabRepository sportTabRepository,
      List<SportTabsTemplate> templates,
      TrendingTabRepository trendingTabRepository,
      PopularTabRepository popularTabRepository) {
    super(sportTabRepository);
    this.sportTabRepository = sportTabRepository;
    this.templates = templates;
    this.trendingTabRepository = trendingTabRepository;
    this.popularTabRepository = popularTabRepository;
  }

  public List<SportTab> findAll(String brand, Integer sportId) {
    return sportTabRepository.findAllByBrandAndSportIdOrderBySortOrderAsc(brand, sportId);
  }

  /**
   * can retrieve disabled tabs
   *
   * @deprecated use findAllForCheckingEvents (with brand specification)
   */
  @Deprecated
  public List<SportTab> findWithEnabledCheckEvents(String tabName) {
    return sportTabRepository.findAllByNameAndCheckEventsTrue(tabName);
  }

  public List<SportTab> findAllForCheckingEvents(String brand, SportTabNames tabName) {
    return sportTabRepository.findActiveWithCheckEventsTrue(brand, tabName.nameLowerCase());
  }

  public List<SportTab> findAllEnabledTabsByName(String brand, SportTabNames tabName) {
    return sportTabRepository.findAllByBrandAndNameAndEnabledTrue(brand, tabName.nameLowerCase());
  }

  public void updateHasEvents(
      String brand, Integer sportId, SportTabNames tabName, boolean hasEvents) {
    sportTabRepository
        .findAllByBrandAndSportIdAndName(brand, sportId, tabName.nameLowerCase())
        .forEach(sportTab -> updateSportTabHasEvent(sportTab, hasEvents));
  }

  private void updateSportTabHasEvent(SportTab sportTab, boolean hasEvents) {
    if (sportTab.isCheckEvents() && sportTab.isHasEvents() != hasEvents) {
      sportTab.setHasEvents(hasEvents);
      sportTabRepository.save(sportTab);
    }
  }

  @Override
  public SportTab prepareModelBeforeSave(SportTab model) {
    if (TABS_WITHOUT_CHECK_EVENTS_FUNCTIONALITY.contains(model.getName())) {
      model.setCheckEvents(false);
    }
    return model;
  }

  public void deleteTabs(SportCategory sportCategory) {
    sportTabRepository.deleteByBrandAndSportId(
        sportCategory.getBrand(), sportCategory.getCategoryId());
  }

  public void createTabs(SportCategory sportCategory) {
    List<SportTab> tabs =
        templates.stream()
            .filter(template -> template.isValidForSport(sportCategory))
            .findFirst()
            .map(template -> template.buildTabs(sportCategory))
            .orElse(Collections.emptyList());

    if (!tabs.isEmpty()) {
      this.save(tabs);
      log.info(
          "SportTab: saved. sportCategory.ssCategoryCode={}. tabs={}",
          sportCategory.getSsCategoryCode(),
          tabs);
    } else {
      log.warn(
          "SportTab: not saved. sportCategory with name={} and id={} "
              + "and ssCategoryCode={} and categoryId={} has not configured any tabs template",
          sportCategory.getImageTitle(),
          sportCategory.getId(),
          sportCategory.getSsCategoryCode(),
          sportCategory.getCategoryId());
    }
  }

  public boolean areThereEventsInCategoryBasedOnSportTabs(SportCategory category) {
    List<SportTab> sportTabs =
        sportTabRepository.findAllByBrandAndSportIdAndEnabledTrue(
            category.getBrand(), category.getCategoryId());
    // 1. SportCategories without sportTabs might be general (e. g. All sports, In-Play etc)
    // 2. Not general sportCategories (Movies etc.) might have wrong sportTab configs (should be
    // deleted/created)
    return sportTabs.isEmpty()
        || (sportTabs.stream()
            .anyMatch(sportTab -> sportTab.isCheckEvents() && sportTab.isHasEvents()));
  }

  public void saveTrendingTabForPopularBets(SportTab sportTab) {
    if (SportTabNames.POPULARBETS.nameLowerCase().equalsIgnoreCase(sportTab.getName())) {
      Optional.ofNullable(sportTab.getTrendingTabs())
          .ifPresent(
              (List<TrendingTab> trendingTabs) -> {
                List<TrendingTab> savedTrendingTabs =
                    trendingTabs.stream()
                        .map(
                            (TrendingTab tab) -> {
                              Optional.ofNullable(tab.getPopularTabs())
                                  .ifPresent(
                                      (List<PopularTab> popularTabs) ->
                                          tab.setPopularTabs(
                                              popularTabs.stream()
                                                  .map(
                                                      (PopularTab pt) -> {
                                                        pt.setBrand(sportTab.getBrand());
                                                        pt.setSportId(sportTab.getSportId());
                                                        return popularTabRepository.save(pt);
                                                      })
                                                  .collect(Collectors.toList())));
                              tab.setBrand(sportTab.getBrand());
                              tab.setSportId(sportTab.getSportId());
                              return trendingTabRepository.save(tab);
                            })
                        .collect(Collectors.toList());
                sportTab.setTrendingTabs(savedTrendingTabs);
              });
    }
  }
}
