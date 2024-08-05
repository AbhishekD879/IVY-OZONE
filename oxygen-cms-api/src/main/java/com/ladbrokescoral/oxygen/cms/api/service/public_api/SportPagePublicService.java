package com.ladbrokescoral.oxygen.cms.api.service.public_api;

import static com.ladbrokescoral.oxygen.cms.api.entity.AbstractSportEntity.SPORT_HOME_PAGE;
import static java.util.Collections.emptyList;
import static java.util.Objects.nonNull;
import static java.util.stream.Collectors.groupingBy;

import com.ladbrokescoral.oxygen.cms.api.dto.*;
import com.ladbrokescoral.oxygen.cms.api.entity.*;
import com.ladbrokescoral.oxygen.cms.api.entity.segment.Segment;
import com.ladbrokescoral.oxygen.cms.api.entity.segment.SegmentConstants;
import com.ladbrokescoral.oxygen.cms.api.mapping.*;
import com.ladbrokescoral.oxygen.cms.api.repository.SegmentRepository;
import com.ladbrokescoral.oxygen.cms.api.service.*;
import com.ladbrokescoral.oxygen.cms.util.Util;
import java.time.Duration;
import java.time.Instant;
import java.time.temporal.ChronoUnit;
import java.util.*;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.stream.Collectors;
import java.util.stream.Stream;
import lombok.RequiredArgsConstructor;
import lombok.SneakyThrows;
import lombok.extern.slf4j.Slf4j;
import org.modelmapper.ModelMapper;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

@Slf4j
@Service
@RequiredArgsConstructor
public class SportPagePublicService {

  private static final SportGroupKey HOME_PAGE_GROUP_KEY =
      new SportGroupKey(SPORT_HOME_PAGE, PageType.sport);
  private static final SportGroupKey CUSTOMIZED_HOME_PAGE_GROUP_KEY =
      new SportGroupKey(SPORT_HOME_PAGE, PageType.customized);
  private static final SportPageId FEATURED_PAGE_ID =
      new SportPageId(SPORT_HOME_PAGE, PageType.sport, SportModuleType.FEATURED);
  private static final SportPageId UNGROUPED_FEATURED_PAGE_ID =
      new SportPageId(SPORT_HOME_PAGE, PageType.sport, SportModuleType.UNGROUPED_FEATURED);
  private static final String FANZONE_WIDGET = "FANZONE_WIDGET";

  @Value("${aem.banners.produce}")
  private boolean produceAemBanners;

  @Value("${last.view.seconds:5}")
  private int lastFewSeconds;

  private final ModularContentPublicService modularContentPublicService;
  private final SportQuickLinkPublicService quickLinkPublicService;
  private final SportModuleService sportModuleService;
  private final HighlightCarouselPublicService highlightCarouselPublicService;
  private final SurfaceBetPublicService surfaceBetPublicService;
  private final StructureService structureService;
  private final RacingModuleMapper racingModuleMapper;
  private final SegmentRepository segmentRepository;
  private final FanzonesService fanzonesService;
  private final VirtualNextEventsService virtualNextEventsService;
  private final BybWidgetPublicService bybWidgetPublicService;
  private final LuckyDipModuleService luckyDipModuleService;
  private final PopularAccaWidgetPublicService popularAccaWidgetPublicService;
  private static final String FANZONE_PAGE_ID = "160";

  /**
   * Grabs all the {@link SportModule}s and their corresponding data and transforms it to {@link
   * SportPage}s perilously grouping data by {@link SportModule#getSportId()}} and {@link
   * SportModule#getModuleType()}. RACING_MODULES should be returned as is (deactivated as well)
   */
  public List<SportPage> findAllPagesByBrand(String brand, long lastUpdateDate) {
    Map<SportPageId, SportModuleDto> moduleByPageId =
        sportModuleService.findByBrand(brand).stream()
            .filter(m -> !m.isDisabled() || SportModuleType.RACING_MODULE.equals(m.getModuleType()))
            .collect(
                Collectors.toMap(SportPageId::fromSportModule, SportModuleMapper.INSTANCE::toDto));

    List<SportPageModuleDataItem> allModuleItems = findByBrand(brand);
    Map<SportPageId, List<SportPageModuleDataItem>> moduleItemsByPageId =
        allModuleItems.stream()
            // Need rework #PR-1491
            // .filter() is just added to quickFix NPE - when modules don't have sportPageId
            // the issue must be investigated deeper RC should be fixed
            .filter(mi -> Objects.nonNull(mi.sportPageId()))
            .collect(groupingBy(SportPageModuleDataItem::sportPageId));

    Map<SportGroupKey, List<SportPageModule>> groupedMap =
        moduleByPageId.keySet().stream()
            .filter(pageId -> nonNull(moduleItemsByPageId.get(pageId)))
            .map(
                pageId ->
                    new SportPageModule(
                        moduleByPageId.get(pageId), moduleItemsByPageId.get(pageId)))
            .collect(groupingBy(sportPageModule -> sportPageModule.getSportModule().getGroupKey()));

    if (isGroupedFeaturedEnabled(brand)) {
      List<SportPageModuleDataItem> featuredModuleItems =
          moduleItemsByPageId.getOrDefault(FEATURED_PAGE_ID, emptyList());
      SportModuleDto keyEventsPageModule = moduleByPageId.get(UNGROUPED_FEATURED_PAGE_ID);
      List<SportPageModule> customizedPageModules =
          getCustomizedPageModules(
              groupedMap.getOrDefault(HOME_PAGE_GROUP_KEY, emptyList()),
              keyEventsPageModule,
              featuredModuleItems);
      if (!customizedPageModules.isEmpty()) {
        groupedMap.put(CUSTOMIZED_HOME_PAGE_GROUP_KEY, customizedPageModules);
      }
    }

    return groupedMap.keySet().stream()
        .map(
            sportGroupKey ->
                createSportPage(sportGroupKey, groupedMap.get(sportGroupKey), lastUpdateDate))
        .collect(Collectors.toList());
  }

  private SportPage createSportPage(
      SportGroupKey sportGroupKey, List<SportPageModule> modules, long lastUpdateDate) {
    boolean isSegmented =
        ((sportGroupKey.getPageId().equals("0"))
            || (sportGroupKey.getPageId().equals(FANZONE_PAGE_ID)));

    return new SportPage(
        String.valueOf(sportGroupKey.getGroupKey()),
        sortedPageModules(modules),
        sportGroupKey.getPageType(),
        sportGroupKey.getPageId(),
        isFeatureStructureChanged(modules, isSegmented, lastUpdateDate),
        isSegmented);
  }

  private List<SportPageModule> sortedPageModules(List<SportPageModule> sportPageModules) {
    return sportPageModules.stream()
        .sorted(
            Comparator.comparing(
                sportPageModule -> sportPageModule.getSportModule().getSortOrder()))
        .collect(Collectors.toList());
  }

  @SneakyThrows
  private List<SportPageModuleDataItem> findByBrand(String brand) {
    CompletableFuture<List<BaseModularContentDto>> featuredData =
        CompletableFuture.supplyAsync(() -> modularContentPublicService.findByBrand(brand));
    CompletableFuture<List<SportQuickLinkDto>> quickLinksData =
        CompletableFuture.supplyAsync(() -> quickLinkPublicService.findAll(brand));
    CompletableFuture<List<InPlayConfigDto>> inPlayModuleData = getInPlayModuleData(brand);
    CompletableFuture<List<RecentlyPlayedGameDto>> rpgModuleData =
        CompletableFuture.supplyAsync(
                () ->
                    sportModuleService.findAllActive(brand, SportModuleType.RECENTLY_PLAYED_GAMES))
            .thenApplyAsync(
                rpgModules ->
                    rpgModules.stream()
                        .map(RecentlyPlayedGameMapper.getInstance()::toDto)
                        .collect(Collectors.toList()));
    CompletableFuture<List<HighlightCarouselDto>> highlightCarouselModuleData =
        CompletableFuture.supplyAsync(
            () -> highlightCarouselPublicService.findActiveByBrand(brand));
    CompletableFuture<List<SurfaceBetDto>> surfaceBetModuleData =
        CompletableFuture.supplyAsync(
            () ->
                surfaceBetPublicService.findActiveByBrandAndRelationType(
                    brand, new AtomicInteger(0), RelationType.sport, RelationType.eventhub));

    CompletableFuture<List<AemBannersDto>> aemBannersData = getAemBannersData(brand);

    CompletableFuture<List<RacingModuleDto>> racingModulesData = getRacingModulesData(brand);

    CompletableFuture<List<VirtualNextEventDto>> nextEventsDto =
        CompletableFuture.supplyAsync(() -> virtualNextEventsService.readByBrandAndActive(brand));

    CompletableFuture<List<PopularBetDto>> popularBetDto = getPopularBetDto(brand);

    CompletableFuture<List<BybWidgetModuleDto>> bybWidgetModuleDto = getBybWidgetModuleDto(brand);

    CompletableFuture<List<LuckyDipModuleDto>> luckyDipModuleData =
        CompletableFuture.supplyAsync(() -> luckyDipModuleService.getLuckyDipModuleData(brand));

    CompletableFuture<List<SuperButtonDto>> superButtonDto = getSuperButtonDto(brand);

    CompletableFuture<List<PopularAccaModuleDto>> popularAccaModuleDto =
        getPopularAccaModuleDto(brand);

    return CompletableFuture.allOf(featuredData, quickLinksData)
        .thenApply(
            nothing ->
                Util.mergeLists(
                    featuredData.join(),
                    quickLinksData.join(),
                    inPlayModuleData.join(),
                    rpgModuleData.join(),
                    highlightCarouselModuleData.join(),
                    surfaceBetModuleData.join(),
                    aemBannersData.join(),
                    racingModulesData.join(),
                    nextEventsDto.join(),
                    popularBetDto.join(),
                    getTeamBetsData(brand).join(),
                    getFanBetsData(brand).join(),
                    bybWidgetModuleDto.join(),
                    luckyDipModuleData.join(),
                    superButtonDto.join(),
                    popularAccaModuleDto.join()))
        .get();
  }

  private CompletableFuture<List<AemBannersDto>> getAemBannersData(String brand) {
    return CompletableFuture.supplyAsync(
            () -> {
              List<SportModule> modules;
              if (produceAemBanners) {
                modules = sportModuleService.findAllActive(brand, SportModuleType.AEM_BANNERS);
              } else {
                log.warn("AEM banners modules were disabled.");
                modules = emptyList();
              }
              return modules;
            })
        .thenApplyAsync(
            modules ->
                modules.stream()
                    .filter(
                        module -> module.getModuleConfig().getDisplayTo().isAfter(Instant.now()))
                    .map(AemBannerDataMapper.INSTANCE::toDto)
                    .collect(Collectors.toList()));
  }

  private CompletableFuture<List<InPlayConfigDto>> getInPlayModuleData(String brand) {
    return CompletableFuture.supplyAsync(
            () -> sportModuleService.findAll(brand, SportModuleType.INPLAY))
        .thenApplyAsync(
            sportModules ->
                sportModules.stream()
                    .map(sportModule -> castToDto(sportModule, brand))
                    .collect(Collectors.toList()));
  }

  private CompletableFuture<List<BybWidgetModuleDto>> getBybWidgetModuleDto(String brand) {
    return CompletableFuture.supplyAsync(
        () -> bybWidgetPublicService.getBybWidgetModuleDtosByBrand(brand));
  }

  private CompletableFuture<List<PopularAccaModuleDto>> getPopularAccaModuleDto(String brand) {
    return CompletableFuture.supplyAsync(
        () -> popularAccaWidgetPublicService.getPopularAccaModuleDtosByBrand(brand));
  }

  private CompletableFuture<List<RacingModuleDto>> getRacingModulesData(String brand) {
    return CompletableFuture.supplyAsync(
            () -> sportModuleService.findAll(brand, SportModuleType.RACING_MODULE))
        .thenApplyAsync(
            modules ->
                modules.stream().map(racingModuleMapper::toDto).collect(Collectors.toList()));
  }

  private CompletableFuture<List<PopularBetDto>> getPopularBetDto(String brand) {
    return CompletableFuture.supplyAsync(
            () -> sportModuleService.findAllActive(brand, SportModuleType.POPULAR_BETS))
        .thenApplyAsync(
            popularBetModle ->
                popularBetModle.stream()
                    .map(m -> new ModelMapper().map(m, PopularBetDto.class))
                    .collect(Collectors.toList()));
  }

  private CompletableFuture<List<SuperButtonDto>> getSuperButtonDto(String brand) {
    return CompletableFuture.supplyAsync(
            () -> sportModuleService.findAllActive(brand, SportModuleType.SUPER_BUTTON))
        .thenApplyAsync(
            superButton ->
                superButton.stream()
                    .map(m -> new SuperButtonDto(m.getSportId()))
                    .collect(Collectors.toList()));
  }

  private CompletableFuture<List<TeamBetsDto>> getTeamBetsData(String brand) {
    return CompletableFuture.supplyAsync(
            () -> sportModuleService.findAll(brand, SportModuleType.BETS_BASED_ON_YOUR_TEAM))
        .thenApplyAsync(
            (List<SportModule> modules) -> {
              List<String> teamIds =
                  fanzonesService
                      .findAllFanzonesByBrand(brand)
                      .map(
                          fanzones ->
                              fanzones.stream()
                                  .parallel()
                                  .filter(Fanzone::getActive)
                                  .filter(
                                      f -> f.getFanzoneConfiguration().getShowBetsBasedOnYourTeam())
                                  .map(Fanzone::getTeamId)
                                  .collect(Collectors.toList()))
                      .orElse(Collections.emptyList());
              return modules.stream()
                  .map(
                      (SportModule module) -> {
                        TeamBetsDto teamBetsDto = TeamBetsMapper.INSTANCE.toDto(module);
                        teamBetsDto.setFanzoneSegments(teamIds);
                        return teamBetsDto;
                      })
                  .collect(Collectors.toList());
            });
  }

  private CompletableFuture<List<FanBetsDto>> getFanBetsData(String brand) {

    return CompletableFuture.supplyAsync(
            () -> sportModuleService.findAll(brand, SportModuleType.BETS_BASED_ON_OTHER_FANS))
        .thenApplyAsync(
            (List<SportModule> modules) -> {
              List<String> teamIds =
                  fanzonesService
                      .findAllFanzonesByBrand(brand)
                      .map(
                          fanzones ->
                              fanzones.stream()
                                  .parallel()
                                  .filter(Fanzone::getActive)
                                  .filter(
                                      f ->
                                          f.getFanzoneConfiguration().getShowBetsBasedOnOtherFans())
                                  .map(Fanzone::getTeamId)
                                  .collect(Collectors.toList()))
                      .orElse(Collections.emptyList());
              return modules.stream()
                  .map(
                      (SportModule module) -> {
                        FanBetsDto fanBetsDto = FanBetsMapper.INSTANCE.toDto(module);
                        fanBetsDto.setFanzoneSegments(teamIds);
                        return fanBetsDto;
                      })
                  .collect(Collectors.toList());
            });
  }

  private InPlayConfigDto castToDto(SportModule sportModule, String brand) {
    InPlayConfigDto dto =
        InPlayConfigMapper.INSTANCE
            .toDto(sportModule.getInplayConfig())
            .setSportId(sportModule.getSportId());

    List<String> segments =
        segmentRepository.findByBrand(brand).stream()
            .map(Segment::getSegmentName)
            .collect(Collectors.toList());
    if (!segments.contains(SegmentConstants.UNIVERSAL)) segments.add(SegmentConstants.UNIVERSAL);

    if ("0".equals(sportModule.getPageId())) {

      List<InplaySportDto> inplaySportDtos =
          sportModule.getInplayConfig().getHomeInplaySports().stream()
              .map(
                  (HomeInplaySport homeInplay) ->
                      HomePageInPlayMapper.getInstance().toDto(homeInplay, segments))
              .collect(Collectors.toList());
      dto.setHomeInplaySports(inplaySportDtos);
    }
    return dto;
  }

  private boolean isGroupedFeaturedEnabled(String brand) {
    return structureService
        .findValueByProperty(brand, "NativeConfig", "isGroupedFeaturedOnHomePageEnabled")
        .filter(Boolean.class::isInstance)
        .map(Boolean.class::cast)
        .orElse(false);
  }

  private List<SportPageModule> getCustomizedPageModules(
      List<SportPageModule> pageModules,
      SportModuleDto ungroupedPageModule,
      List<SportPageModuleDataItem> featuredModuleItems) {
    List<SportPageModule> customizedPageModules = shallowCopy(pageModules);

    if (nonNull(ungroupedPageModule)) {
      customizedPageModules.add(
          new SportPageModule(
              ungroupedPageModule, toUngroupedFeaturedModuleItems(featuredModuleItems)));
    }

    // remove extra modules from FEATURED
    customizedPageModules.stream()
        .filter(
            pageModule -> pageModule.getSportModule().getModuleType() == SportModuleType.FEATURED)
        .map(SportPageModule::getPageData)
        .flatMap(this::featuredModularContentStream)
        .forEach(
            modularContent ->
                modularContent.setModuleDtos(
                    sortAndGroupBySport(
                        modularContent.getModuleDtos().stream()
                            .filter(ModuleDto::isGroupedBySport)
                            .map(moduleDto -> moduleDto.toBuilder().build())
                            .collect(Collectors.toList()))));
    return customizedPageModules;
  }

  private List<SportPageModuleDataItem> toUngroupedFeaturedModuleItems(
      List<SportPageModuleDataItem> featuredModuleItems) {
    return featuredModularContentStream(featuredModuleItems)
        .map(ModularContentDto::copy)
        .map(
            (ModularContentDto modularContent) -> {
              List<ModuleDto> keyModuleDtos =
                  modularContent.getModuleDtos().stream()
                      .filter(moduleDto -> !moduleDto.isGroupedBySport())
                      .collect(Collectors.toList());
              modularContent.setModuleDtos(keyModuleDtos);
              return modularContent;
            })
        .filter(modularContent -> !modularContent.getModuleDtos().isEmpty())
        .collect(Collectors.toList());
  }

  private List<ModuleDto> sortAndGroupBySport(List<ModuleDto> moduleDtos) {
    AtomicInteger displayOrder = new AtomicInteger(0);
    return moduleDtos.stream()
        .sorted(
            Comparator.comparing(
                ModuleDto::getDisplayOrder, Comparator.nullsLast(Comparator.naturalOrder())))
        .collect(
            groupingBy(
                moduleDto ->
                    Optional.ofNullable(moduleDto.getData())
                        .map(Collection::stream)
                        .orElse(Stream.empty())
                        .findFirst()
                        .map(ModuleDataDto::getCategoryId)
                        .orElse("uncategorized"),
                LinkedHashMap::new,
                Collectors.toList()))
        .values()
        .stream()
        .flatMap(Collection::stream)
        .map(
            (ModuleDto moduleDto) -> {
              moduleDto.setDisplayOrder(Double.valueOf(displayOrder.getAndIncrement()));
              return moduleDto;
            })
        .collect(Collectors.toList());
  }

  private Stream<ModularContentDto> featuredModularContentStream(
      List<SportPageModuleDataItem> featuredModuleItems) {
    return featuredModuleItems.stream()
        .filter(ModularContentDto.class::isInstance)
        .map(ModularContentDto.class::cast)
        .filter(modularContent -> "Featured".equals(modularContent.getDirectiveName()));
  }

  private List<SportPageModule> shallowCopy(List<SportPageModule> pageModules) {
    return pageModules.stream()
        .map(
            pageModule ->
                new SportPageModule(
                    createCustomModule(pageModule.getSportModule()),
                    pageModule.getPageData().stream()
                        .map(this::copyModule)
                        .collect(Collectors.toList())))
        .collect(Collectors.toList());
  }

  private SportModuleDto createCustomModule(SportModuleDto module) {
    SportModuleDto customModule = SportModuleMapper.INSTANCE.copy(module);
    customModule.setPageType(PageType.customized);
    customModule.setId(PageType.customized.getPrefix() + module.getSportId() + module.getId());
    return customModule;
  }

  private SportPageModuleDataItem copyModule(SportPageModuleDataItem moduleItem) {
    if (moduleItem instanceof ModularContentDto) {
      return ((ModularContentDto) moduleItem).copy();
    }
    if (moduleItem instanceof Copyable) {
      String prefix = PageType.customized.getPrefix() + moduleItem.sportPageId().getId();
      Copyable<SportPageModuleDataItem> item = (Copyable<SportPageModuleDataItem>) moduleItem;
      return item.copy(PageType.customized, prefix);
    }
    return moduleItem;
  }

  private boolean isFeatureStructureChanged(
      List<SportPageModule> modules, boolean isSegmented, long lastUpdateDate) {
    return modules.stream()
        .filter(
            module ->
                (isSegmented
                    && (module
                            .getSportModule()
                            .getModuleType()
                            .equals(SportModuleType.HIGHLIGHTS_CAROUSEL)
                        || module
                            .getSportModule()
                            .getModuleType()
                            .equals(SportModuleType.FEATURED))))
        .anyMatch(
            module ->
                isFeatureStructureChanged(
                    module.getPageData(), module.getSportModule(), lastUpdateDate));
  }

  private boolean isFeatureStructureChanged(
      List<SportPageModuleDataItem> data, SportModuleDto sportModule, long lastUpdateDate) {
    if (SportModuleType.HIGHLIGHTS_CAROUSEL.equals(sportModule.getModuleType())) {
      return data.stream()
          .map(HighlightCarouselDto.class::cast)
          .flatMap(moduleDto -> moduleDto.getSegmentReferences().stream())
          .anyMatch(
              segmentReferenceDto ->
                  isSegmentReferenceupdated(segmentReferenceDto, lastUpdateDate));
    } else {
      return data.stream()
          .filter(ModularContentDto.class::isInstance)
          .map(ModularContentDto.class::cast)
          .flatMap(modularContentDto -> modularContentDto.getModuleDtos().stream())
          .flatMap(moduleDto -> moduleDto.getSegmentReferences().stream())
          .anyMatch(
              segmentReferenceDto ->
                  isSegmentReferenceupdated(segmentReferenceDto, lastUpdateDate));
    }
  }

  private boolean isSegmentReferenceupdated(
      SegmentReferenceDto segmentReferenceDto, long lastUpdateDate) {

    if (lastUpdateDate == 0) return checkUpdatedInLastFiveSeconds(segmentReferenceDto);
    return checkUpdateWithLastRun(segmentReferenceDto, lastUpdateDate);
  }

  private boolean checkUpdatedInLastFiveSeconds(SegmentReferenceDto segmentReferenceDto) {
    Instant now = Instant.now().truncatedTo(ChronoUnit.SECONDS);
    Instant updatedAt = segmentReferenceDto.getUpdatedAt().truncatedTo((ChronoUnit.SECONDS));
    return Duration.between(updatedAt, now).getSeconds() < lastFewSeconds;
  }

  private boolean checkUpdateWithLastRun(
      SegmentReferenceDto segmentReferenceDto, long lastUpdateDate) {
    Instant updatedAt = segmentReferenceDto.getUpdatedAt();
    Instant now = Instant.now();
    return Duration.between(updatedAt, now).toMillis() < now.toEpochMilli() - lastUpdateDate;
  }
}
