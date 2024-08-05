package com.ladbrokescoral.oxygen.cms.api.service.public_api;

import static com.ladbrokescoral.oxygen.cms.api.service.public_api.ModuleRibbonTabPublicService.BUILD_YOUR_BET_TAB;

import com.ladbrokescoral.oxygen.cms.api.dto.BaseModularContentDto;
import com.ladbrokescoral.oxygen.cms.api.dto.HomeModuleSegmentedDto;
import com.ladbrokescoral.oxygen.cms.api.dto.ModularContentDto;
import com.ladbrokescoral.oxygen.cms.api.dto.ModularIdsContentDto;
import com.ladbrokescoral.oxygen.cms.api.dto.ModularSegmentedContentDto;
import com.ladbrokescoral.oxygen.cms.api.dto.ModuleDataDto;
import com.ladbrokescoral.oxygen.cms.api.dto.ModuleDto;
import com.ladbrokescoral.oxygen.cms.api.dto.ModuleRibbonTabSegmentedDto;
import com.ladbrokescoral.oxygen.cms.api.dto.SportPageId;
import com.ladbrokescoral.oxygen.cms.api.entity.AbstractSportEntity;
import com.ladbrokescoral.oxygen.cms.api.entity.DataSelection;
import com.ladbrokescoral.oxygen.cms.api.entity.DeviceType;
import com.ladbrokescoral.oxygen.cms.api.entity.HomeModule;
import com.ladbrokescoral.oxygen.cms.api.entity.ModuleRibbonTab;
import com.ladbrokescoral.oxygen.cms.api.entity.PageType;
import com.ladbrokescoral.oxygen.cms.api.entity.SportModuleType;
import com.ladbrokescoral.oxygen.cms.api.entity.segment.Segment;
import com.ladbrokescoral.oxygen.cms.api.entity.segment.SegmentConstants;
import com.ladbrokescoral.oxygen.cms.api.mapping.HomeModuleMapper;
import com.ladbrokescoral.oxygen.cms.api.mapping.ModularContentMapper;
import com.ladbrokescoral.oxygen.cms.api.mapping.ModuleRibbonTabMapper;
import com.ladbrokescoral.oxygen.cms.api.repository.SegmentRepository;
import com.ladbrokescoral.oxygen.cms.api.service.ApiService;
import com.ladbrokescoral.oxygen.cms.api.service.BybTabAvailabilityService;
import com.ladbrokescoral.oxygen.cms.api.service.ModuleRibbonTabService;
import com.ladbrokescoral.oxygen.cms.api.service.SegmentService;
import com.ladbrokescoral.oxygen.cms.api.service.SegmentedModuleSerive;
import com.ladbrokescoral.oxygen.cms.api.service.impl.HomeModuleServiceImpl;
import java.math.BigInteger;
import java.util.Collections;
import java.util.EnumMap;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;
import java.util.Map.Entry;
import java.util.Optional;
import java.util.Set;
import java.util.function.Function;
import java.util.stream.Collectors;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.mapstruct.factory.Mappers;
import org.springframework.stereotype.Service;
import org.springframework.util.CollectionUtils;

@Slf4j
@Service
@RequiredArgsConstructor
public class ModularContentPublicService implements ApiService<BaseModularContentDto> {

  public static final String FEATURED_DIRECTIVE = "Featured";
  private static final String HORSE_RACING_CATEGORY_ID = "21";
  private final HomeModuleServiceImpl homeModuleService;
  private final ModuleRibbonTabService moduleRibbonTabService;
  private final BybTabAvailabilityService bybTabAvailabilityService;
  private final BuildYourBetPublicService buildYourBetPublicService;
  private final SegmentRepository segmentRepository;
  private final SegmentedModuleSerive segmentedModuleSerive;
  private final SegmentService segmentService;

  public List<BaseModularContentDto> findByBrand(String brand) {
    boolean bybAvailable = bybTabAvailabilityService.isBybEnabledAndLeaguesAvailable(brand);
    return findModularContent(brand, bybAvailable, false);
  }

  public List<HomeModule> findPersonalised(String brand) {

    return homeModuleService
        .findByActiveStateAndPublishToChannelAndApplyUniversalSegments(true, brand).stream()
        .filter(HomeModule::isPersonalised)
        .collect(Collectors.toList());
  }

  public List<BaseModularContentDto> prepareInitialDataModularContent(String brand) {
    boolean displayBuildYourBet = isDisplayBuildYourBet(brand);
    return findInitialDataModularContent(brand, displayBuildYourBet);
  }

  public List<BaseModularContentDto> findInitialDataModularContent(
      String brand, boolean displayBuildYourBet) {
    return findModularContent(brand, displayBuildYourBet, true);
  }

  private List<BaseModularContentDto> findModularContent(
      String brand, boolean displayBuildYourBet, boolean removeFeaturedModules) {
    List<ModuleRibbonTab> ribbonTabs = getRibbonTabs(brand, displayBuildYourBet);
    List<HomeModule> homeModules = getHomeModules(brand);
    return mapModuleContents(brand, ribbonTabs, homeModules, removeFeaturedModules);
  }

  private List<ModuleRibbonTab> getRibbonTabs(String brand, boolean displayBuildYourBet) {
    List<ModuleRibbonTab> ribbonTabs = moduleRibbonTabService.findAllByBrandAndVisible(brand);
    if (!displayBuildYourBet) {
      ribbonTabs =
          ribbonTabs.stream()
              .filter(ribbonTab -> !BUILD_YOUR_BET_TAB.equals(ribbonTab.getInternalId()))
              .collect(Collectors.toList());
    }
    return ribbonTabs;
  }

  private List<HomeModule> getHomeModules(String brand) {
    List<HomeModule> homeModules =
        homeModuleService.findByActiveStateAndPublishToChannel(true, brand);
    return homeModules.stream()
        .filter(homeModule -> !homeModule.isPersonalised())
        .collect(Collectors.toList());
  }

  private List<BaseModularContentDto> mapModuleContents(
      String brand,
      List<ModuleRibbonTab> ribbonTabs,
      List<HomeModule> homeModules,
      boolean removeFeaturedModules) {
    ModularContentMapper mapper = Mappers.getMapper(ModularContentMapper.class);

    List<BaseModularContentDto> allList = new LinkedList<>();

    // data from this elements are intended to be used by IdsCollector class in
    // oxygen-middleware
    // (featured-consumer)
    // for now, only enhMultiplesIds & racingEventsIds are been used.
    // verify if we still need this data in featured-consumer, if no, remove ASAP
    Map<PageType, Set<String>> homeModulesPages =
        homeModules.stream()
            .collect(
                Collectors.groupingBy(
                    HomeModule::getPageType,
                    Collectors.mapping(HomeModule::getPageId, Collectors.toSet())));

    Map<PageType, Map<String, ModularIdsContentDto>> eventsData =
        initEventsDataPerPage(homeModulesPages);

    ModuleContentParameters params =
        ModuleContentParameters.builder()
            .brand(brand)
            .ribbonTabs(ribbonTabs)
            .homeModules(homeModules)
            .removeFeaturedModules(removeFeaturedModules)
            .mapper(mapper)
            .allList(allList)
            .eventsData(eventsData)
            .build();

    mapModuleContent(params);

    // eventsData should always be a last element in list
    // (Featured Midleware selects First Featured Module to Process)
    // (FE issue, problems with parsing ModularContent in other case)
    allList.addAll(
        eventsData.values().stream()
            .flatMap(m -> m.values().stream())
            .collect(Collectors.toList()));

    return allList;
  }

  private Map<PageType, Map<String, ModularIdsContentDto>> initEventsDataPerPage(
      Map<PageType, Set<String>> homeModulesPages) {
    // Featured page should always be present
    homeModulesPages.compute(
        PageType.sport,
        (sport, pageIds) -> {
          if (CollectionUtils.isEmpty(pageIds)) {
            return Collections.singleton(AbstractSportEntity.SPORT_HOME_PAGE);
          }
          pageIds.add(AbstractSportEntity.SPORT_HOME_PAGE);
          return pageIds;
        });

    Map<PageType, Map<String, ModularIdsContentDto>> eventDataMap = new EnumMap<>(PageType.class);
    for (Entry<PageType, Set<String>> pageTypeEntry : homeModulesPages.entrySet()) {
      eventDataMap.put(
          pageTypeEntry.getKey(),
          pageTypeEntry.getValue().stream()
              .collect(
                  Collectors.toMap(
                      Function.identity(),
                      pageId -> createEventsData(pageTypeEntry.getKey(), pageId))));
    }
    return eventDataMap;
  }

  private ModularIdsContentDto createEventsData(PageType pageType, String pageId) {
    return ModularIdsContentDto.builder()
        .sportPageId(new SportPageId(pageId, pageType, SportModuleType.FEATURED))
        .build();
  }

  @Data
  @Builder
  @AllArgsConstructor
  private static class ModuleContentParameters {

    private String brand;
    private List<ModuleRibbonTab> ribbonTabs;
    private List<HomeModule> homeModules;
    private boolean removeFeaturedModules;
    private ModularContentMapper mapper;
    private List<BaseModularContentDto> allList;
    private Map<PageType, Map<String, ModularIdsContentDto>> eventsData;

    public ModularIdsContentDto getEventsData(PageType pageType, String pageId) {
      return eventsData.getOrDefault(pageType, Collections.emptyMap()).get(pageId);
    }
  }

  private void mapModuleContent(ModuleContentParameters params) {

    for (ModuleRibbonTab tab : params.getRibbonTabs()) {
      ModularContentDto mappedTab = params.getMapper().toDto(tab);
      if (isFeatured(mappedTab.getDirectiveName())) {
        params.getAllList().add(handleFeaturedTab(mappedTab, params, PageType.sport, null));
      } else if (isRelatedToEventHub(mappedTab.getDirectiveName())) {
        String pageId = String.valueOf(tab.getHubIndex());
        mappedTab.sportPageId(new SportPageId(pageId, PageType.eventhub, SportModuleType.FEATURED));
        params.getAllList().add(handleFeaturedTab(mappedTab, params, PageType.eventhub, pageId));
      } else {
        params.getAllList().add(mappedTab);
      }
    }
  }

  private ModularContentDto handleFeaturedTab(
      ModularContentDto mappedTab,
      ModuleContentParameters params,
      PageType pageType,
      String pageId) {
    return CollectionUtils.isEmpty(params.getHomeModules())
        ? mappedTab
        : updateTabWithHomeModuleData(mappedTab, params, pageType, pageId);
  }

  /**
   * We need this method for backward compatibility - for any microservice, that still uses Public
   * API of {brand}/modular-content type - this method adds "modules" section for Featured tab,
   * which has all Featured modules configured on cms for homepage for respective brand.
   *
   * <p>Required for oxygen-middleware up to release-96.0.0
   *
   * <p>To be removed, since {brand}/sport-pages API serves same purpose.
   */
  private ModularContentDto updateTabWithHomeModuleData(
      ModularContentDto mappedTab,
      ModuleContentParameters params,
      PageType pageType,
      String pageId) {
    for (HomeModule module : params.getHomeModules()) {
      if (isRelatedToSport(module, pageType)) {
        populateFeaturedData(params, mappedTab, module);
      } else if (isRelatedToEventHub(module, pageId)) {
        populateFeaturedData(params, mappedTab, module);
      } else {
        log.trace("Unsupported navItem {} in homeModule {}", module.getNavItem(), module.getId());
      }
    }
    return mappedTab;
  }

  private boolean isRelatedToSport(HomeModule module, PageType pageType) {
    return isFeatured(module.getNavItem())
        && PageType.sport.equals(module.getPageType())
        && PageType.sport.equals(pageType);
  }

  private boolean isRelatedToEventHub(HomeModule module, String pageId) {
    return PageType.eventhub.equals(module.getPageType())
        && (pageId != null && pageId.equals(module.getPageId()));
  }

  /**
   * fill all *Ids collections in ModularIdsContentDto, and populate "modules" field in Featured tab
   */
  private void populateFeaturedData(
      ModuleContentParameters params, ModularContentDto featuredTab, HomeModule module) {
    List<String> segments =
        segmentRepository.findByBrand(params.getBrand()).stream()
            .map(Segment::getSegmentName)
            .collect(Collectors.toList());
    if (!segments.contains(SegmentConstants.UNIVERSAL)) segments.add(SegmentConstants.UNIVERSAL);
    ModuleDto mappedModuleDto = params.getMapper().toDto(module, params.getBrand(), segments);
    for (ModuleDataDto item : mappedModuleDto.getData()) {
      item.setOutcomeStatus(false);
      item.setOutcomeId(null);
      populateEventsData(
          params.getEventsData(mappedModuleDto.getPageType(), mappedModuleDto.getPageId()),
          module,
          item);
    }
    if (!params.isRemoveFeaturedModules()) {
      featuredTab.addModulesItem(mappedModuleDto);
    }
  }

  private void populateEventsData(
      ModularIdsContentDto eventsData, HomeModule module, ModuleDataDto item) {
    DataSelection dataSelection = module.getDataSelection();
    String selectionType = dataSelection.getSelectionType();
    Integer itemId = Optional.ofNullable(item.getId()).map(Integer::valueOf).orElse(null);

    item.setOutcomeStatus(false);

    if (selectionType.equals("Selection")) {
      eventsData.addOutcomesIdsItem(new BigInteger(dataSelection.getSelectionId()));
      item.setMarketsCount(null);
      item.setOutcomeStatus(true);
      item.setOutcomeId(new BigInteger(dataSelection.getSelectionId()));
    }
    if (selectionType.equals("Type")) {
      if (item.isOutright()) {
        eventsData.addTypeIdsItem(Integer.valueOf(dataSelection.getSelectionId()));
      } else {
        eventsData.addEventsIdsItem(itemId);
      }
    }
    if (selectionType.equals("RaceTypeId")) {
      eventsData.addRacingEventsIdsItem(itemId);
    }
    if (selectionType.contains("Enhanced Multiples")) {
      eventsData.addEnhMultiplesIdsItem(itemId);
    }
    if (selectionType.equals("Market")) {
      eventsData.addMarketIdsItem(Integer.valueOf(dataSelection.getSelectionId()));
      item.setMarketId(dataSelection.getSelectionId());
      if (HORSE_RACING_CATEGORY_ID.equals(item.getCategoryId())) {
        eventsData.addRacingEventsIdsItem(itemId);
      }
    }
    if (selectionType.equals("Event")) {
      eventsData.addEventsIdsItem(itemId);
    }
  }

  private boolean isFeatured(String element) {
    return FEATURED_DIRECTIVE.equalsIgnoreCase(element);
  }

  private boolean isRelatedToEventHub(String element) {
    return "EventHub".equalsIgnoreCase(element);
  }

  public List<BaseModularContentDto> prepareSegmentedInitialDataModularContent(
      String brand, String segmentName, DeviceType device) {
    boolean displayBuildYourBet = isDisplayBuildYourBet(brand);
    return findSegmentedInitialDataModularContent(brand, displayBuildYourBet, segmentName, device);
  }

  private boolean isDisplayBuildYourBet(String brand) {
    return bybTabAvailabilityService.isBuildYourBetConfigurationEnabled(brand, false)
        && buildYourBetPublicService.isAtLeastOneBanachEventAvailable(brand);
  }

  public List<BaseModularContentDto> findSegmentedInitialDataModularContent(
      String brand, boolean displayBuildYourBet, String segmentName, DeviceType deviceType) {

    if (!SegmentConstants.UNIVERSAL.equals(segmentName)) {
      segmentName =
          segmentedModuleSerive.isSegmentedModule(
                  ModuleRibbonTab.class.getSimpleName(), deviceType, brand)
              ? segmentName
              : SegmentConstants.UNIVERSAL;
    }
    return findSegmentedModularContent(brand, displayBuildYourBet, true, segmentName);
  }

  private List<BaseModularContentDto> findSegmentedModularContent(
      String brand,
      boolean displayBuildYourBet,
      boolean removeFeaturedModules,
      String segmentName) {
    List<ModuleRibbonTab> ribbonTabs =
        getSegmentedRibbonTabs(brand, displayBuildYourBet, segmentName);
    List<HomeModule> homeModules = getSegmentedHomeModules(brand, segmentName);
    return mapModuleContents(brand, ribbonTabs, homeModules, removeFeaturedModules);
  }

  private List<ModuleRibbonTab> getSegmentedRibbonTabs(
      String brand, boolean displayBuildYourBet, String segmentName) {
    List<ModuleRibbonTab> ribbonTabs =
        moduleRibbonTabService.findAllSegmentedByBrandAndVisible(brand, segmentName);
    if (!displayBuildYourBet) {
      ribbonTabs =
          ribbonTabs.stream()
              .filter(ribbonTab -> !BUILD_YOUR_BET_TAB.equals(ribbonTab.getInternalId()))
              .collect(Collectors.toList());
    }
    return ribbonTabs;
  }

  private List<HomeModule> getSegmentedHomeModules(String brand, String segmentName) {
    List<HomeModule> homeModules =
        homeModuleService.findByActiveStateAndPublishToChannelBySegmantName(
            true, brand, segmentName);
    return homeModules.stream()
        .filter(homeModule -> !homeModule.isPersonalised())
        .collect(Collectors.toList());
  }

  public List<BaseModularContentDto> findUniversalByBrand(String brand) {
    boolean bybAvailable = bybTabAvailabilityService.isBybEnabledAndLeaguesAvailable(brand);
    return findSegmentedModularContent(brand, bybAvailable, false, SegmentConstants.UNIVERSAL);
  }

  public List<ModuleRibbonTab> findAllVisibleModuleRibbon(String brand) {
    return moduleRibbonTabService.findAllByBrandAndVisible(brand);
  }

  public ModularSegmentedContentDto preparesModularContentCollection(String brand) {

    List<String> segments = segmentService.getSegmentsForSegmentedViews(brand);

    List<ModuleRibbonTabSegmentedDto> moduleRibbonTabSegmentedDto =
        findAllVisibleModuleRibbon(brand).stream()
            .map(e -> ModuleRibbonTabMapper.INSTANCE.toSegmentedDto(e, segments))
            .collect(Collectors.toList());

    List<HomeModuleSegmentedDto> homeModuleSegmentedDto =
        homeModuleService.findByActiveStateAndPublishToChannel(true, brand).stream()
            .map(e -> HomeModuleMapper.INSTANCE.toSegmentedDto(e, segments))
            .collect(Collectors.toList());

    return ModularSegmentedContentDto.builder()
        .displayBuildYourBet(isDisplayBuildYourBet(brand))
        .moduleRibbonTabCollection(moduleRibbonTabSegmentedDto)
        .homeModuleCollection(homeModuleSegmentedDto)
        .build();
  }
}
