package com.coral.oxygen.middleware.featured.consumer;

import static com.coral.oxygen.middleware.pojos.model.cms.EventLoadingType.RACING_GRID;
import static com.coral.oxygen.middleware.pojos.model.output.featured.FeaturedRawIndex.PageType.customized;
import static org.apache.commons.lang3.BooleanUtils.isNotTrue;
import static org.apache.commons.lang3.BooleanUtils.isTrue;

import com.coral.oxygen.cms.api.CmsService;
import com.coral.oxygen.middleware.common.service.AssetManagementService;
import com.coral.oxygen.middleware.common.service.ModuleAdapter;
import com.coral.oxygen.middleware.common.service.featured.OddsCardHeader;
import com.coral.oxygen.middleware.featured.configuration.FeaturedConfiguration;
import com.coral.oxygen.middleware.featured.consumer.sportpage.*;
import com.coral.oxygen.middleware.featured.consumer.sportpage.bets.PopularBetModuleProcessor;
import com.coral.oxygen.middleware.featured.consumer.sportpage.virtual.VirtualEventsModuleProcessor;
import com.coral.oxygen.middleware.featured.service.*;
import com.coral.oxygen.middleware.pojos.model.cms.CmsSystemConfig;
import com.coral.oxygen.middleware.pojos.model.cms.featured.*;
import com.coral.oxygen.middleware.pojos.model.output.EventsModuleData;
import com.coral.oxygen.middleware.pojos.model.output.featured.*;
import com.coral.oxygen.middleware.pojos.model.output.featured.FeaturedRawIndex.VersionedPageKey;
import com.coral.oxygen.middleware.pojos.model.output.featured.RpgConfig;
import java.math.BigDecimal;
import java.time.Duration;
import java.time.Instant;
import java.util.*;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.function.Function;
import java.util.regex.Pattern;
import java.util.stream.Collectors;
import java.util.stream.Stream;
import lombok.Data;
import lombok.extern.slf4j.Slf4j;
import org.apache.commons.lang3.StringUtils;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.util.CollectionUtils;

@Slf4j
@Data
public class FeaturedDataConsumer extends ModuleAdapter implements ModuleConsumer<EventsModule> {
  private static final String COMMA_DELIMITER = ",";
  private static final String HOMEPAGE_ID = "0";
  private static final String CUSTOMIZED_HOMEPAGE_ID = customized.getPrefix() + HOMEPAGE_ID;
  public static final String HIGHLIGHTCAROUSELMODULE = "HighlightCarouselModule";
  public static final String SURFACEBETMODULE = "SurfaceBetModule";

  public static final String QUICKLINKMODULE = "QuickLinkModule";
  public static final String TEAMBETSMODULE = "TeamBetsModule";
  public static final String FANBETSMODULE = "FanBetsModule";
  private static final String TEAM_SEPERATOR_REGEX = " vs | v ";
  private static final Pattern TEAM_SEPERATOR_PATTERN =
      Pattern.compile(TEAM_SEPERATOR_REGEX, Pattern.CASE_INSENSITIVE);

  private static final Comparator<AbstractFeaturedModule<?>> FEATURED_MODULE_COMPARATOR =
      Comparator.comparing(
              (Function<AbstractFeaturedModule<?>, BigDecimal>)
                  AbstractFeaturedModule::getDisplayOrder,
              Comparator.nullsLast(Comparator.naturalOrder()))
          .thenComparing(
              AbstractFeaturedModule::getSecondaryDisplayOrder,
              Comparator.nullsLast(Comparator.naturalOrder()));
  public static final int TEAM_SIZE = 2;

  private final CmsService cmsService;
  private final BybService bybService;

  private final HighlightCarouselModuleProcessor highlightCarouselModuleProcessor;
  private final FanzoneHighlightCarouselModuleProcessor fanzonehighlightCarouselModuleProcessor;
  private final SurfaceBetModuleProcessor surfaceBetModuleProcessor;
  private final FanzoneSurfaceBetModuleProcessor fanzoneSurfaceBetModuleProcessor;
  private final InplayModuleConsumer inplayModuleConsumer;
  private final FeaturedModuleProcessor featuredModuleProcessor;
  private final AemCarouselsProcessor aemCarouselsProcessor;
  private final QuickLinkModuleProcessor quickLinkModuleProcessor;
  private final FanzoneQuickLinkModuleProcessor fanzoneQuickLinkModuleProcessor;
  private final RacingModuleProcessor racingModuleProcessor;
  private final TeamBetsFZModuleProcessor teamBetsFZModuleProcessor;
  private final FanBetsFZModuleProcessor fanBetsFZModuleProcessor;
  private final VirtualEventsModuleProcessor virtualEventsModuleProcessor;
  private final PopularBetModuleProcessor popularBetModuleProcessor;
  private final BybWidgetProcessor bybWidgetProcessor;
  private final LuckyDipModuleProcessor luckyDipModuleProcessor;
  private final PopularAccaModuleProcessor popularAccaModuleProcessor;

  private FeaturedDataFilter featuredDataFilter;
  private OddsCardHeader oddsCardHeader;
  private OutcomeOrdering outcomeOrdering = new OutcomeOrdering();
  private SportPageFilter sportPageFilter;
  private FeaturedModelStorageService storageService;
  private AssetManagementService assetManagementService;
  private FeaturedNextRacesConfigProcessor nextRacesConfigProcessor;

  @Value("${cms.fanzone.pageid}")
  private String fanzonePageId;

  private static final String TWO_UP_MARKET = "2UpMarket";

  @Value("${market.template.twoUpResult}")
  private String twoUpResultString;

  public FeaturedDataConsumer(FeaturedConfiguration config) {
    this.cmsService = config.getCmsService();
    this.featuredDataFilter = config.getFeaturedDataFilter();
    this.oddsCardHeader = config.getOddsCardHeader();
    this.bybService = config.getBybService();
    this.sportPageFilter = config.getSportPageFilter();
    this.highlightCarouselModuleProcessor = config.getHighlightCarouselModuleProcessor();
    this.fanzonehighlightCarouselModuleProcessor =
        config.getFanzonehighlightCarouselModuleProcessor();
    this.inplayModuleConsumer = config.getInplayModuleConsumer();
    this.surfaceBetModuleProcessor = config.getSurfaceBetModuleProcessor();
    this.fanzoneSurfaceBetModuleProcessor = config.getFanzoneSurfaceBetModuleProcessor();
    this.featuredModuleProcessor = config.getFeaturedModuleProcessor();
    this.aemCarouselsProcessor = config.getAemCarouselsProcessor();
    this.quickLinkModuleProcessor = config.getQuickLinkModuleProcessor();
    this.fanzoneQuickLinkModuleProcessor = config.getFanzoneQuickLinkModuleProcessor();
    racingModuleProcessor = config.getRacingModuleProcessor();
    this.storageService = config.getStorageService();
    this.assetManagementService = config.getAssetManagementService();
    this.nextRacesConfigProcessor = config.getNextRacesConfigProcessor();
    this.teamBetsFZModuleProcessor = config.getTeamBetsFZModuleProcessor();
    this.fanBetsFZModuleProcessor = config.getFanBetsFZModuleProcessor();
    this.virtualEventsModuleProcessor = config.getVirtualEventsModuleProcessor();
    this.popularBetModuleProcessor = config.getPopularBetModuleProcessor();
    this.bybWidgetProcessor = config.getBybWidgetProcessor();
    this.luckyDipModuleProcessor = config.getLuckyDipModuleProcessor();
    this.popularAccaModuleProcessor = config.getPopularAccaModuleProcessor();
  }

  public FeaturedModelsData consumeInParallels() {
    assetManagementService.clearLastGenerationTeams();
    List<SportPage> pages = getSportPages();
    if (pages.isEmpty()) {
      return new FeaturedModelsData();
    }

    bybService.reloadData();
    CmsSystemConfig cmsConfig = cmsService.requestSystemConfig();
    ExecutorService service = Executors.newSingleThreadExecutor();
    service.submit(() -> this.nextRacesConfigProcessor.processNextRaces(cmsConfig));
    service.shutdown();

    // aemCarouselsProcessor.populateBannersBucket();  enable this if AEM is required to get banners

    List<FeaturedModel> featuredModels =
        pages.parallelStream()
            .filter(page -> !CollectionUtils.isEmpty(page.getSportPageModules()))
            .map(page -> createFeaturedModel(page, cmsConfig))
            .filter(featuredModel -> !CollectionUtils.isEmpty(featuredModel.getModules()))
            .collect(Collectors.toCollection(ArrayList::new));
    return new FeaturedModelsData(featuredModels, pages);
  }

  private FeaturedModel createFeaturedModel(SportPage page, CmsSystemConfig cmsConfig) {
    VersionedPageKey index = VersionedPageKey.fromPage(page.getSportId());
    List<Long> excludedEvents = new LinkedList<>();
    Stream<AbstractFeaturedModule<?>> stream =
        page.getSportPageModules().stream()
            .filter(Objects::nonNull)
            .sorted(ModulePrioritizer.SPORT_PAGE_MODULE_COMPARATOR)
            .flatMap(
                m ->
                    createModule(m, cmsConfig, excludedEvents)
                        .map(
                            sportModule -> {
                              // translate to integer index, additional info
                              // oxygen-cms-api::SportPagePublicService::sortedPageModules
                              sportModule.setDisplayOrder(
                                  new BigDecimal(page.getSportPageModules().indexOf(m)));
                              return sportModule;
                            }))
            .map(
                module -> {
                  excludedEvents.addAll(ModuleEventIdParser.getEventIds(module));

                  return module;
                });

    if (CUSTOMIZED_HOMEPAGE_ID.equals(page.getPageId())) {
      stream = stream.sorted(Comparator.comparing(AbstractFeaturedModule::getDisplayOrder));
    } else {
      stream = stream.sorted(FEATURED_MODULE_COMPARATOR);
    }
    List<AbstractFeaturedModule<?>> modules =
        stream.collect(Collectors.toCollection(ArrayList::new));

    FeaturedModel featuredModel =
        FeaturedModel.builder()
            .directiveName(index.getType().toString())
            .modules(modules)
            .pageId(index.getPageId())
            .visible(true)
            .title(index.getPageId() + " " + index.getType() + " page")
            // field "showTabOn" not configurable from UI, should always be "both"
            .showTabOn("both")
            .featureStructureChanged(page.isFeatureStructureChanged())
            .segmented(page.isSegmented())
            .useFSCCached(cmsConfig.isUseFSCCachedEnabled())
            .build();
    if (StringUtils.isNotBlank(fanzonePageId)
        && fanzonePageId.equals(page.getPageId())) { // Fanzone BMA-62182
      log.info("Fanzone Page ID loaded from Properties :" + fanzonePageId);
      Map<String, FanzoneSegmentView> fanzoneSegmentWiseModules =
          page.isSegmented() ? createFanzoneSegmentwiseModules(featuredModel) : null;
      featuredModel.setFanzoneSegmentWiseModules(fanzoneSegmentWiseModules);
    } else {
      Map<String, SegmentView> segmentWiseModules =
          page.isSegmented() ? createSegmentwiseModules(featuredModel) : null;
      featuredModel.setSegmentWiseModules(segmentWiseModules);
    }
    return featuredModel;
  }

  private List<SportPage> getSportPages() {
    Long lastRunTime = storageService.getLastRunTime();
    Collection<SportPage> requestPages =
        Objects.isNull(lastRunTime)
            ? cmsService.requestPages()
            : cmsService.requestPages(lastRunTime);
    List<SportPage> pages =
        requestPages.stream()
            .filter(sportPageFilter::isSupportedPage)
            .collect(Collectors.toCollection(ArrayList::new));

    log.info("Consumed {} sport pages, after filtering are {}", requestPages.size(), pages.size());
    if (requestPages.size() != pages.size()) {
      requestPages.removeAll(pages);
      String filteredIds = getCommaSeparatedSportIds(requestPages);
      log.info("Filtered sportIds : {} ", filteredIds);
    }

    String ids = getCommaSeparatedSportIds(pages);
    log.info("Going to process sportIds : {} ", ids);
    return pages;
  }

  private String getCommaSeparatedSportIds(Collection<SportPage> requestPages) {
    return requestPages.stream()
        .map(SportPage::getSportId)
        .collect(Collectors.joining(COMMA_DELIMITER));
  }

  private Stream<AbstractFeaturedModule<?>> createModule(
      SportPageModule cmsModule, CmsSystemConfig cmsSystemConfig, List<Long> excludedEventIds) {
    long s = System.currentTimeMillis();
    if (cmsModule.getSportModule().getModuleType() == null) {
      return Stream.empty();
    }

    final Set<Long> excludedEvents = Collections.unmodifiableSet(new HashSet<>(excludedEventIds));

    List<AbstractFeaturedModule<?>> thisModules = new ArrayList<>();
    try {
      switch (cmsModule.getSportModule().getModuleType()) {
        case FEATURED, UNGROUPED_FEATURED:
          thisModules.addAll(processModules(cmsModule, cmsSystemConfig, excludedEvents));
          break;
        case QUICK_LINK:
          if (StringUtils.isNotBlank(fanzonePageId)
              && fanzonePageId.equals(cmsModule.getSportModule().getPageId())) {
            thisModules.add(
                fanzoneQuickLinkModuleProcessor.processModule(
                    cmsModule, cmsSystemConfig, excludedEvents));
          } else {
            thisModules.add(
                quickLinkModuleProcessor.processModule(cmsModule, cmsSystemConfig, excludedEvents));
          }
          break;
        case INPLAY:
          thisModules.add(
              inplayModuleConsumer.processModule(cmsModule, cmsSystemConfig, excludedEvents));
          break;
        case HIGHLIGHTS_CAROUSEL:
          List<HighlightCarouselModule> result;
          if (StringUtils.isNotBlank(fanzonePageId)
              && fanzonePageId.equals(cmsModule.getSportModule().getPageId())) {
            result =
                fanzonehighlightCarouselModuleProcessor.processModules(
                    cmsModule, cmsSystemConfig, excludedEvents);
          } else {
            result =
                highlightCarouselModuleProcessor.processModules(
                    cmsModule, cmsSystemConfig, excludedEvents);
          }
          thisModules.addAll(processEventsModules(result, cmsSystemConfig));
          highlightCarouselModuleProcessor.applyLimits(thisModules);
          addAssetManagementData(thisModules);
          break;
        case SURFACE_BET:
          thisModules.addAll(getSurfaceBetModule(cmsModule, cmsSystemConfig, excludedEvents));
          break;
        case RECENTLY_PLAYED_GAMES:
          thisModules.add(getRPGModule(cmsModule));
          break;
        case AEM_BANNERS:
          thisModules.add(
              aemCarouselsProcessor.processModule(cmsModule, cmsSystemConfig, excludedEvents));
          break;
        case RACING_MODULE:
          thisModules.addAll(
              racingModuleProcessor.processModules(cmsModule, cmsSystemConfig, excludedEvents));
          break;
        case BETS_BASED_ON_OTHER_FANS:
          thisModules.add(
              fanBetsFZModuleProcessor.processModule(cmsModule, cmsSystemConfig, excludedEvents));

          break;
        case BETS_BASED_ON_YOUR_TEAM:
          thisModules.add(
              teamBetsFZModuleProcessor.processModule(cmsModule, cmsSystemConfig, excludedEvents));
          break;
        case VIRTUAL_NEXT_EVENTS:
          List<VirtualEventModule> virtualEventModules =
              virtualEventsModuleProcessor.processModules(cmsModule, null, null);
          thisModules.addAll(processVirtualEventsModules(virtualEventModules, cmsSystemConfig));
          virtualEventsModuleProcessor.applyLimits(thisModules);
          break;
        case POPULAR_BETS:
          List<PopularBetModule> popularBetModules =
              popularBetModuleProcessor.processModules(cmsModule);
          thisModules.addAll(popularBetModules);
          break;
        case BYB_WIDGET:
          thisModules.add(
              bybWidgetProcessor.processModule(cmsModule, cmsSystemConfig, excludedEvents));
          addAssetManagementDataForBybModule(thisModules);

          break;
        case SUPER_BUTTON:
          thisModules.add(getSuperButton(cmsModule));
          break;
        case LUCKY_DIP:
          thisModules.add(
              luckyDipModuleProcessor.processModule(cmsModule, cmsSystemConfig, excludedEvents));
          break;
        case POPULAR_ACCA:
          thisModules.add(
              popularAccaModuleProcessor.processModule(cmsModule, cmsSystemConfig, excludedEvents));
          break;
        default:
          log.error("Unknown featured module type {}", cmsModule.getPageData());
      }
      return thisModules.stream()
          .filter(Objects::nonNull)
          .filter(module -> module.getErrorMessage() == null)
          .filter(AbstractFeaturedModule::isValid);
    } catch (Exception e) {
      log.error(
          "Failed to create AbstractFeaturedModule from cms module {}",
          cmsModule.getSportModule().getModuleType(),
          e);
      return Stream.empty();
    } finally {
      log.info(
          "PAGE {} Module {} time {}",
          cmsModule.getSportModule().getPageId(),
          cmsModule.getSportModule().getModuleType(),
          System.currentTimeMillis() - s);
    }
  }

  private List<SurfaceBetModule> getSurfaceBetModule(
      SportPageModule cmsModule, CmsSystemConfig cmsSystemConfig, Set<Long> excludedEvents) {
    SurfaceBetModule surfaceBetModule;
    if (StringUtils.isNotBlank(fanzonePageId)
        && fanzonePageId.equals(cmsModule.getSportModule().getPageId())) {
      surfaceBetModule =
          fanzoneSurfaceBetModuleProcessor.processModule(
              cmsModule, cmsSystemConfig, excludedEvents);
    } else {
      surfaceBetModule =
          surfaceBetModuleProcessor.processModule(cmsModule, cmsSystemConfig, excludedEvents);
    }
    List<SurfaceBetModule> validatedSurfaceBetModules =
        Stream.of(surfaceBetModule).collect(Collectors.toCollection(ArrayList::new));
    filterEventDataModules(
        validatedSurfaceBetModules,
        cmsSystemConfig,
        "0".equals(cmsModule.getSportModule().getPageId()));
    if (!validatedSurfaceBetModules.isEmpty()) {
      updateBuildYourBet(surfaceBetModule.getData());
      surfaceBetModuleProcessor.postProcessModule(surfaceBetModule);
    }
    return validatedSurfaceBetModules;
  }

  @Override
  public List<EventsModule> processModules(
      SportPageModule cmsModule, CmsSystemConfig cmsSystemConfig, Set<Long> excludedEventIds) {
    List<ModularContentItem> items =
        cmsModule.getPageData().stream()
            .map(ModularContentItem.class::cast)
            .collect(Collectors.toCollection(ArrayList::new));
    List<EventsModule> featuredModules =
        featuredModuleProcessor.getFirstFeaturedEventModules(
            cmsModule.getSportModule(), new ModularContent(items), excludedEventIds);
    processFeaturedEventsModules(
        featuredModules, cmsSystemConfig, cmsModule.getSportModule().getSportId() == 0);
    featuredModules.forEach(module -> module.setSportId(cmsModule.getSportModule().getSportId()));
    return featuredModules;
  }

  private RecentlyPlayedGameModule getRPGModule(SportPageModule cmsModule) {
    RecentlyPlayedGameModule rpgModule = new RecentlyPlayedGameModule(cmsModule.getSportModule());
    List<RpgConfig> data =
        cmsModule.getPageData().stream()
            .map(cmsData -> (RecentlyPlayedGame) cmsData)
            .map(RpgConfig::new)
            .collect(Collectors.toCollection(ArrayList::new));
    rpgModule.setData(data);
    return rpgModule;
  }

  private SuperButtonModule getSuperButton(SportPageModule cmsModule) {
    SuperButtonModule superButtonModule = new SuperButtonModule(cmsModule.getSportModule());
    List<SuperButtonConfig> data =
        cmsModule.getPageData().stream()
            .map(cmsData -> (SuperButton) cmsData)
            .map(SuperButtonConfig::new)
            .collect(Collectors.toCollection(ArrayList::new));
    superButtonModule.setData(data);
    return superButtonModule;
  }

  private void filterEventDataModules(
      List<? extends AbstractFeaturedModule<? extends EventsModuleData>> eventsModules,
      CmsSystemConfig cmsSystemConfig) {
    featuredDataFilter.removeOlderEvents(eventsModules, cmsSystemConfig);
    featuredDataFilter.removeNotLiveservedLiveEvents(eventsModules);
    featuredDataFilter.removeEmptyNodes(eventsModules);
    orderEvents(eventsModules);
    orderOutcomes(eventsModules);
    clearNameOverrides(eventsModules);
  }

  private void filterEventDataModules(
      List<? extends AbstractFeaturedModule<? extends EventsModuleData>> eventsModules,
      CmsSystemConfig cmsSystemConfig,
      boolean isSegmented) {
    featuredDataFilter.removeOlderEvents(eventsModules, cmsSystemConfig);
    featuredDataFilter.removeNotLiveservedLiveEvents(eventsModules);
    featuredDataFilter.removeEmptyNodes(eventsModules);
    if (isSegmented) {
      orderEventsWithOnlyDisplayOrder(eventsModules);
    } else {
      orderEvents(eventsModules);
    }
    orderOutcomes(eventsModules);
    clearNameOverrides(eventsModules);
  }

  private List<? extends EventsModule> processEventsModules(
      List<? extends EventsModule> eventsModules, CmsSystemConfig cmsSystemConfig) {
    filterEventDataModules(eventsModules, cmsSystemConfig);

    truncateEventsToMaxCount(eventsModules);
    calculateOutcomeCoulumnsHeaders(eventsModules);
    truncateOutcomesToMaxCount(eventsModules);
    calculateHasNoLiveEvents(eventsModules);

    eventsModules.stream()
        .filter(AbstractFeaturedModule::isErrorEmpty)
        .forEach(
            module -> {
              final List<EventsModuleData> eventsModuleData = module.getData();
              module.setCashoutAvail(featuredDataFilter.isCashOutAvailable(eventsModuleData));
              updateBuildYourBet(eventsModuleData);
            });
    return eventsModules;
  }

  private List<? extends EventsModule> processVirtualEventsModules(
      List<? extends EventsModule> eventsModules, CmsSystemConfig cmsSystemConfig) {
    filterVirtualEventDataModules(eventsModules, cmsSystemConfig);

    truncateEventsToMaxCount(eventsModules);
    calculateOutcomeCoulumnsHeaders(eventsModules);
    truncateOutcomesToMaxCount(eventsModules);
    calculateHasNoLiveEvents(eventsModules);

    eventsModules.stream()
        .filter(AbstractFeaturedModule::isErrorEmpty)
        .forEach(
            (EventsModule module) -> {
              final List<EventsModuleData> eventsModuleData = module.getData();
              module.setCashoutAvail(featuredDataFilter.isCashOutAvailable(eventsModuleData));
            });
    return eventsModules;
  }

  private List<? extends EventsModule> processFeaturedEventsModules(
      List<? extends EventsModule> eventsModules,
      CmsSystemConfig cmsSystemConfig,
      boolean segmented) {

    filterEventDataModules(eventsModules, cmsSystemConfig);
    if (!segmented) truncateEventsToMaxCount(eventsModules);
    calculateOutcomeCoulumnsHeaders(eventsModules);
    truncateOutcomesToMaxCount(eventsModules);
    calculateHasNoLiveEvents(eventsModules);

    eventsModules.stream()
        .filter(AbstractFeaturedModule::isErrorEmpty)
        .forEach(
            (EventsModule module) -> {
              final List<EventsModuleData> eventsModuleData = module.getData();
              if (!segmented)
                module.setCashoutAvail(featuredDataFilter.isCashOutAvailable(eventsModuleData));
              updateBuildYourBet(eventsModuleData);
            });
    return eventsModules;
  }

  private void clearNameOverrides(
      List<? extends AbstractFeaturedModule<? extends EventsModuleData>> eventsModules) {
    eventsModules.stream()
        .map(AbstractFeaturedModule::getData)
        .flatMap(List::stream)
        .forEach(data -> data.setNameOverride(null));
  }

  private void updateBuildYourBet(List<? extends EventsModuleData> eventsModuleData) {
    eventsModuleData.forEach(
        event -> {
          boolean isBybAvailable =
              bybService.isBuildYourBetAvailableForType(Long.parseLong(event.getTypeId()));
          event.setBuildYourBetAvailable(isBybAvailable);
        });
  }

  protected void calculateOutcomeCoulumnsHeaders(List<? extends EventsModule> eventsModules) {
    eventsModules.forEach(
        module ->
            module.setOutcomeColumnsTitles(oddsCardHeader.calculateHeadTitles(module.getData())));
  }

  private void calculateHasNoLiveEvents(List<? extends EventsModule> eventsModules) {
    eventsModules.stream()
        .filter(EventsModule::isErrorEmpty)
        .filter(module -> RACING_GRID.isTypeOf(module.getDataSelection().getSelectionType()))
        .forEach(module -> module.setHasNoLiveEvents(true));

    eventsModules.stream()
        .filter(EventsModule::isErrorEmpty)
        .filter(module -> !RACING_GRID.isTypeOf(module.getDataSelection().getSelectionType()))
        .forEach(
            module ->
                module.setHasNoLiveEvents(
                    module.getData().stream()
                        .anyMatch(event -> !Boolean.TRUE.equals(event.getEventIsLive()))));
  }

  private void truncateEventsToMaxCount(List<? extends EventsModule> eventsModules) {
    eventsModules.stream()
        .filter(m -> m.getMaxRows() != null && m.getMaxRows() > 0)
        .forEach(m -> m.setData(truncated(m.getData(), m.getMaxRows())));
  }

  private void truncateOutcomesToMaxCount(List<? extends EventsModule> eventsModules) {
    eventsModules.stream()
        .filter(m -> m.getMaxSelections() != null && m.getMaxSelections() > 0)
        .forEach(
            m ->
                m.getData()
                    .forEach(
                        event ->
                            event
                                .getMarkets()
                                .forEach(
                                    market ->
                                        market.setOutcomes(
                                            truncated(
                                                market.getOutcomes(), m.getMaxSelections())))));
  }

  private <T> List<T> truncated(List<T> list, int maxSize) {
    return list.subList(0, Math.min(list.size(), maxSize));
  }

  private void orderEvents(
      List<? extends AbstractFeaturedModule<? extends EventsModuleData>> eventsModules) {
    eventsModules.stream()
        .filter(this::removeHighLightsCarouselWithEventIds)
        .map(AbstractFeaturedModule::getData)
        .filter(Objects::nonNull)
        .forEach(
            dataList ->
                dataList.sort(
                    Comparator.comparing(
                            EventsModuleData::getEventIsLive,
                            Comparator.nullsLast(Comparator.reverseOrder()))
                        .thenComparing(
                            EventsModuleData::getDisplayOrder,
                            Comparator.nullsLast(Comparator.naturalOrder()))
                        .thenComparing(
                            EventsModuleData::getStartTime,
                            Comparator.nullsLast(Comparator.naturalOrder()))
                        .thenComparing(
                            EventsModuleData::getName,
                            Comparator.nullsLast(Comparator.naturalOrder()))));
  }

  private void filterVirtualEventDataModules(
      List<? extends AbstractFeaturedModule<? extends EventsModuleData>> eventsModules,
      CmsSystemConfig cmsSystemConfig) {
    featuredDataFilter.removeOlderEvents(eventsModules, cmsSystemConfig);
    featuredDataFilter.removeNotLiveservedLiveEvents(eventsModules);
    featuredDataFilter.removeEmptyNodes(eventsModules);
    orderVirtualEvents(eventsModules);
    orderOutcomes(eventsModules);
    clearNameOverrides(eventsModules);
  }

  private void orderVirtualEvents(
      List<? extends AbstractFeaturedModule<? extends EventsModuleData>> eventsModules) {
    eventsModules.stream()
        .map(AbstractFeaturedModule::getData)
        .filter(Objects::nonNull)
        .forEach(
            dataList ->
                dataList.sort(
                    Comparator.comparing(
                            EventsModuleData::getDisplayOrder,
                            Comparator.nullsLast(Comparator.naturalOrder()))
                        .thenComparing(
                            EventsModuleData::getStartTime,
                            Comparator.nullsLast(Comparator.naturalOrder()))
                        .thenComparing(
                            EventsModuleData::getName,
                            Comparator.nullsLast(Comparator.naturalOrder()))));
  }

  private void orderEventsWithOnlyDisplayOrder(
      List<? extends AbstractFeaturedModule<? extends EventsModuleData>> eventsModules) {
    eventsModules.stream()
        .filter(this::removeHighLightsCarouselWithEventIds)
        .map(AbstractFeaturedModule::getData)
        .filter(Objects::nonNull)
        .forEach(
            dataList ->
                dataList.sort(
                    Comparator.comparing(
                        EventsModuleData::getDisplayOrder,
                        Comparator.nullsLast(Comparator.naturalOrder()))));
  }

  private boolean removeHighLightsCarouselWithEventIds(
      AbstractFeaturedModule<? extends EventsModuleData> eventsModule) {
    if (eventsModule instanceof HighlightCarouselModule highlightCarouselModule) {
      return ((highlightCarouselModule.getTypeId() != null)
          || (highlightCarouselModule.getTypeIds() != null)); // Fanzone BMA-62182
    }
    return true;
  }

  private void orderOutcomes(
      List<? extends AbstractFeaturedModule<? extends EventsModuleData>> eventsModules) {
    // Sorting if it's a race
    eventsModules.stream()
        .filter(featuredDataFilter::isRacingGridModule)
        .map(AbstractFeaturedModule::getData)
        .flatMap(List::stream)
        .flatMap(e -> e.getMarkets().stream())
        .forEach(
            m ->
                outcomeOrdering.orderRacingGridOutcomes(
                    m.getOutcomes(), isTrue(m.getSpAvailable()) && isNotTrue(m.getLpAvailable())));

    // Sorting
    eventsModules.stream()
        .filter(module -> featuredDataFilter.isRaceTypeEventModule(module))
        .map(AbstractFeaturedModule::getData)
        .flatMap(List::stream)
        .map(EventsModuleData::getMarkets)
        .flatMap(List::stream)
        .forEach(
            market ->
                outcomeOrdering.orderOutcomes(
                    market.getOutcomes(), isTrue(market.getLpAvailable()), true));
  }

  private Map<String, SegmentView> createSegmentwiseModules(FeaturedModel featuredModel) {
    Instant start = Instant.now();
    Map<String, SegmentView> segmentWiseModules = new HashMap<>();
    Map<String, Set<Long>> segmentedExcludedEvents = new HashMap<>();
    Map<Long, EventsModuleData> eventsModuleData = new HashMap<>();
    try {
      log.info("Processing SegmentwiseModules for page::", featuredModel.getPageId());
      List<AbstractFeaturedModule<?>> modules =
          featuredModel.getModules().stream()
              .sorted(ModulePrioritizer.FEATURE_MODULE_COMPARATOR)
              .map(
                  (AbstractFeaturedModule<?> module) -> {
                    String moduleName = module.getClass().getSimpleName();
                    module.setSegmented(true);
                    switch (moduleName) {
                      case HIGHLIGHTCAROUSELMODULE:
                        {
                          List<String> twoUpmarkets = null;
                          if (TWO_UP_MARKET.equals(
                              ((HighlightCarouselModule) module).getDisplayMarketType())) {
                            twoUpmarkets =
                                Arrays.stream(twoUpResultString.split(","))
                                    .flatMap(n -> Stream.of("|" + n + "|", n))
                                    .collect(Collectors.toCollection(ArrayList::new));
                          }
                          FeaturedConsumerUtil.setEventsModuleData(
                              eventsModuleData, module, twoUpmarkets);
                          highlightCarouselModuleProcessor.processSegmentwiseModules(
                              (HighlightCarouselModule) module,
                              segmentWiseModules,
                              HIGHLIGHTCAROUSELMODULE);
                          setSegmentedExcludedEvents(
                              module, segmentWiseModules, segmentedExcludedEvents);
                          break;
                        }
                      case "EventsModule":
                        {
                          FeaturedConsumerUtil.setEventsModuleData(eventsModuleData, module, null);
                          featuredModuleProcessor.processSegmentwiseModules(
                              (EventsModule) module,
                              segmentWiseModules,
                              segmentedExcludedEvents,
                              "EventsModule");
                          break;
                        }
                      case QUICKLINKMODULE:
                        {
                          quickLinkModuleProcessor.processSegmentwiseModules(
                              (QuickLinkModule) module, segmentWiseModules, QUICKLINKMODULE);
                          featuredModel.setQuickLinkModule((QuickLinkModule) module);
                          break;
                        }
                      case SURFACEBETMODULE:
                        {
                          surfaceBetModuleProcessor.processSegmentwiseModules(
                              (SurfaceBetModule) module, segmentWiseModules, SURFACEBETMODULE);
                          featuredModel.setSurfaceBetModule((SurfaceBetModule) module);
                          break;
                        }
                      case "InplayModule":
                        {
                          FeaturedConsumerUtil.setEventsModuleData(eventsModuleData, module, null);
                          inplayModuleConsumer.processSegmentwiseModules(
                              (InplayModule) module, segmentWiseModules, "InplayModule");
                          inplayModuleConsumer.limitEvents(
                              segmentWiseModules, (InplayModule) module, segmentedExcludedEvents);
                          featuredModel.setInplayModule((InplayModule) module);
                          FeaturedConsumerUtil.removeUnusedSportsSegments((InplayModule) module);
                          setSegmentedExcludedEvents(
                              module, segmentWiseModules, segmentedExcludedEvents);
                          break;
                        }
                      default:
                        module.setSegmented(false);
                        break;
                    }
                    return module;
                  })
              .collect(Collectors.toCollection(ArrayList::new));
      // Need to sort according to display order before saving as the generation
      featuredModel.setModules(
          modules.stream()
              .sorted(FEATURED_MODULE_COMPARATOR)
              .collect(Collectors.toCollection(ArrayList::new)));
      featuredModel.setEventsModuleData(eventsModuleData);
    } catch (Exception e) {
      log.error("Failed to create SegmentwiseModules", e);
      return segmentWiseModules;
    }
    Instant end = Instant.now();
    log.info("time: elapsed time taken {}", Duration.between(end, start).toMillis());
    return segmentWiseModules;
  }
  /**
   * Fanzone BMA-62182: Preparing fanzone segment view for each Fanzone
   *
   * @param featuredModel
   * @return FanzoneSegmented Map
   */
  private Map<String, FanzoneSegmentView> createFanzoneSegmentwiseModules(
      FeaturedModel featuredModel) {
    Instant start = Instant.now();
    Map<String, FanzoneSegmentView> fanzoneSegmentWiseModules = new HashMap<>();
    List<AbstractFeaturedModule<?>> modules = featuredModel.getModules();
    try {
      log.info("Processing FanzoneSegmentwiseModules for page::", featuredModel.getPageId());
      modules.forEach(
          (AbstractFeaturedModule<?> module) -> {
            String moduleName = module.getClass().getSimpleName();
            module.setSegmented(true);
            switch (moduleName) {
              case HIGHLIGHTCAROUSELMODULE:
                {
                  fanzonehighlightCarouselModuleProcessor.processFanzoneSegmentwiseModules(
                      (HighlightCarouselModule) module, fanzoneSegmentWiseModules);
                  break;
                }
              case SURFACEBETMODULE:
                {
                  fanzoneSurfaceBetModuleProcessor.processFanzoneSegmentwiseModules(
                      (SurfaceBetModule) module, fanzoneSegmentWiseModules);
                  featuredModel.setSurfaceBetModule((SurfaceBetModule) module);
                  break;
                }
              case QUICKLINKMODULE:
                {
                  fanzoneQuickLinkModuleProcessor.processFanzoneSegmentwiseModules(
                      (QuickLinkModule) module, fanzoneSegmentWiseModules);
                  featuredModel.setQuickLinkModule((QuickLinkModule) module);
                  break;
                }
              case TEAMBETSMODULE:
                {
                  teamBetsFZModuleProcessor.processFanzoneSegmentwiseModules(
                      (TeamBetsModule) module, fanzoneSegmentWiseModules);
                  featuredModel.setTeamBetsModule((TeamBetsModule) module); // ?
                  break;
                }
              case FANBETSMODULE:
                {
                  fanBetsFZModuleProcessor.processFanzoneSegmentwiseModules(
                      (FanBetsModule) module, fanzoneSegmentWiseModules);
                  featuredModel.setFanBetsModule((FanBetsModule) module); // ?
                  break;
                }
              default:
                module.setSegmented(false);
                break;
            }
          });
    } catch (Exception e) {
      log.error("Failed to create FanzoneSegmentwiseModules", e);
      return fanzoneSegmentWiseModules;
    }
    Instant end = Instant.now();
    log.info(
        "time: elapsed time taken to create FanzoneSegmentwiseModules{}",
        Duration.between(end, start).toMillis());
    return fanzoneSegmentWiseModules;
  }

  private void setSegmentedExcludedEvents(
      AbstractFeaturedModule<?> module,
      Map<String, SegmentView> segmentWiseModules,
      Map<String, Set<Long>> segmentedExcludedEvents) {
    if (module.getModuleType().equals(ModuleType.HIGHLIGHTS_CAROUSEL)) {
      ((HighlightCarouselModule) module)
          .getSegments()
          .forEach(
              (String seg) -> {
                List<Long> events = ModuleEventIdParser.getEventIds(module);
                Set<Long> eventIds =
                    segmentedExcludedEvents.containsKey(seg)
                        ? segmentedExcludedEvents.get(seg)
                        : new HashSet<>();
                eventIds.addAll(events);
                segmentedExcludedEvents.put(seg, eventIds);
              });
    } else {
      segmentWiseModules
          .entrySet()
          .forEach(
              (Map.Entry<String, SegmentView> entry) -> {
                Map<String, SegmentOrderdModuleData> segmentOrderdModuleData =
                    entry.getValue().getInplayModuleData();
                Set<Long> events =
                    segmentOrderdModuleData.values().stream()
                        .filter(data -> data.getEventIds() != null)
                        .map(SegmentOrderdModuleData::getEventIds)
                        .flatMap(Collection::stream)
                        .collect(Collectors.toSet());
                Set<Long> eventIds =
                    segmentedExcludedEvents.containsKey(entry.getKey())
                        ? segmentedExcludedEvents.get(entry.getKey())
                        : new HashSet<>();
                eventIds.addAll(events);
                segmentedExcludedEvents.put(entry.getKey(), eventIds);
              });
    }
  }

  private void addAssetManagementData(List<AbstractFeaturedModule<?>> thisModules) {
    thisModules.stream()
        .filter(HighlightCarouselModule.class::isInstance)
        .map(HighlightCarouselModule.class::cast)
        .flatMap(highlightCarouselModule -> highlightCarouselModule.getData().stream())
        .forEach(assetManagementService::setAssetManagementMetaData);
  }

  private void addAssetManagementDataForBybModule(List<AbstractFeaturedModule<?>> thisModules) {
    thisModules.stream()
        .filter(BybWidgetModule.class::isInstance)
        .map(BybWidgetModule.class::cast)
        .flatMap(bybModule -> bybModule.getData().stream())
        .forEach(assetManagementService::setAssetManagementMetaData);
  }
}
