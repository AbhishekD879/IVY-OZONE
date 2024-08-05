package com.coral.oxygen.middleware.in_play.service;

import static com.coral.oxygen.middleware.in_play.service.injector.InPlayDataInjectorType.*;
import static com.coral.oxygen.middleware.pojos.model.InPlayTopLevelType.LIVE_EVENT;
import static com.coral.oxygen.middleware.pojos.model.InPlayTopLevelType.STREAM_EVENT;
import static com.coral.oxygen.middleware.pojos.model.InPlayTopLevelType.UPCOMING_EVENT;
import static com.coral.oxygen.middleware.pojos.model.InPlayTopLevelType.UPCOMING_STREAM_EVENT;
import static com.coral.oxygen.middleware.pojos.model.output.MarketTemplateType.OUTRIGHT;
import static com.google.common.collect.Maps.transformEntries;
import static java.util.Comparator.comparing;
import static java.util.Comparator.comparingInt;
import static java.util.stream.Collectors.*;
import static org.apache.commons.lang3.BooleanUtils.isTrue;
import static org.springframework.util.CollectionUtils.isEmpty;

import com.coral.oxygen.cms.api.CmsService;
import com.coral.oxygen.df.api.DFService;
import com.coral.oxygen.middleware.common.mappers.EventMapper;
import com.coral.oxygen.middleware.common.mappers.MarketMapper;
import com.coral.oxygen.middleware.common.service.AssetManagementService;
import com.coral.oxygen.middleware.common.service.MarketTemplateNameService;
import com.coral.oxygen.middleware.in_play.service.injector.InPlayDataInjectorFactory;
import com.coral.oxygen.middleware.in_play.service.siteserver.InplaySiteServeService;
import com.coral.oxygen.middleware.pojos.model.InPlayTopLevelType;
import com.coral.oxygen.middleware.pojos.model.cms.CmsInplayData;
import com.coral.oxygen.middleware.pojos.model.cms.SportItem;
import com.coral.oxygen.middleware.pojos.model.cms.VirtualSportDto;
import com.coral.oxygen.middleware.pojos.model.cms.VirtualSportEvents;
import com.coral.oxygen.middleware.pojos.model.df.Horse;
import com.coral.oxygen.middleware.pojos.model.df.RaceEvent;
import com.coral.oxygen.middleware.pojos.model.output.*;
import com.coral.oxygen.middleware.pojos.model.output.inplay.InPlayData;
import com.coral.oxygen.middleware.pojos.model.output.inplay.InPlayModel;
import com.coral.oxygen.middleware.pojos.model.output.inplay.SportSegment;
import com.coral.oxygen.middleware.pojos.model.output.inplay.TypeSegment;
import com.egalacoral.spark.siteserver.model.Category;
import com.egalacoral.spark.siteserver.model.Event;
import java.util.*;
import java.util.function.Function;
import java.util.stream.Collectors;
import lombok.extern.slf4j.Slf4j;
import org.apache.commons.lang3.tuple.Pair;
import org.springframework.beans.BeanUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.cache.Cache;
import org.springframework.cache.CacheManager;
import org.springframework.stereotype.Service;
import org.springframework.util.CollectionUtils;
import org.springframework.util.ObjectUtils;

@Service
@ConditionalOnProperty(name = "inplay.scheduled.task.enabled")
@Slf4j
public class InPlayDataConsumer {

  private final CmsService cmsService;
  private final EventMapper eventMapper;
  private final MarketMapper marketMapper;
  private final InPlayDataFilter inPlayDataFilter;
  private final SportsRibbonService sportsRibbonService;
  private final InPlayDataSorter inPlayDataSorter;
  private final MarketTemplateNameService marketTemplateNameService;
  private final InplaySiteServeService siteServeService;
  private final InPlayDataInjectorFactory dataInjectorFactory;
  private final DFService dfService;
  private final CacheManager cacheManager;
  private final AssetManagementService assetManagementService;

  private static final Integer HR_CATEGORY_ID = 21;
  private static final String HR_CATEGORY_CODE = "HORSE_RACING";
  private static final String EMPTY_STRING = "";

  private static final String VIRTUAL_SPORTS = "virtualSports";
  private static final String VIRTUAL_SPORT_CACHE = "virtualSportsCache";

  @Autowired
  public InPlayDataConsumer(
      CmsService cmsService,
      @Qualifier("inplay") EventMapper eventMapper,
      @Qualifier("inplayMarketMapper") MarketMapper marketMapper,
      InPlayDataFilter inPlayDataFilter,
      SportsRibbonService sportsRibbonService,
      InPlayDataSorter inPlayDataSorter,
      MarketTemplateNameService marketTemplateNameService,
      InPlayDataInjectorFactory dataInjectorFactory,
      InplaySiteServeService siteserverService,
      DFService dfService,
      CacheManager cacheManager,
      AssetManagementService assetManagementService) {
    this.cmsService = cmsService;
    this.eventMapper = eventMapper;
    this.marketMapper = marketMapper;
    this.dataInjectorFactory = dataInjectorFactory;
    this.inPlayDataFilter = inPlayDataFilter;
    this.sportsRibbonService = sportsRibbonService;
    this.inPlayDataSorter = inPlayDataSorter;
    this.marketTemplateNameService = marketTemplateNameService;
    this.siteServeService = siteserverService;
    this.dfService = dfService;
    this.cacheManager = cacheManager;
    this.assetManagementService = assetManagementService;
  }

  public InPlayData consume() {
    assetManagementService.clearLastGenerationTeams();
    CmsInplayData cmsInplayData = cmsService.requestInplayData();

    Set<String> categoryIds =
        cmsInplayData.getActiveSportCategories().stream()
            .map(SportItem::getCategoryId)
            .collect(toSet());

    InPlayData inPlayData = getInPlayDataEvents(categoryIds);

    List<VirtualSportDto> virtualSportDtoCollection =
        (cmsInplayData.getVirtualSports() != null)
            ? cmsInplayData.getVirtualSports()
            : cmsService.getVirtualSportsByBrand();
    log.debug("Virtual Data from CMS :" + virtualSportDtoCollection);
    getVirtualInplayData(inPlayData, virtualSportDtoCollection);
    inPlayDataFilter.removeEmptyNodes(inPlayData);
    inPlayDataSorter.sort(inPlayData);

    dataInjectorFactory.injectorOf(EVENT_COUNT).injectData(inPlayData);
    dataInjectorFactory.injectorOf(EVENT_IDS).injectData(inPlayData);
    CmsInplayData finalCmsInplayData = cmsInplayData;
    dataInjectorFactory.injectorOf(CMS_SPORT_DATA).injectData(inPlayData, () -> finalCmsInplayData);

    // In next injector we add category path - do we need to add on previous step ??
    dataInjectorFactory.injectorOf(SPORTS_CONFIG).injectData(inPlayData);
    dataInjectorFactory.injectorOf(COMMENTARY).injectData(inPlayData);
    dataInjectorFactory.injectorOf(SCORE_BOARD_STATS).injectData(inPlayData);
    dataInjectorFactory.injectorOf(TYPE_SECTION_TITLE).injectData(inPlayData);

    inPlayData.setLiveStream(getLiveStreamInplayModel(inPlayData.getLivenow(), STREAM_EVENT));
    inPlayData.setUpcomingLiveStream(
        getLiveStreamInplayModel(inPlayData.getUpcoming(), UPCOMING_STREAM_EVENT));
    inPlayData.setSportsRibbon(
        sportsRibbonService.createSportsRibbon(
            cmsInplayData.getActiveSportCategories(), inPlayData));
    applyAssetManagementData(inPlayData);
    return inPlayData;
  }

  private void applyAssetManagementData(InPlayData inPlayData) {

    // set assets to inner event modules
    InPlayData.allSportSegmentsStream(inPlayData)
        .forEach(
            (SportSegment sportSegment) ->
                sportSegment.getEventsByTypeName().stream()
                    .map(e -> setAssetToType(e, String.valueOf(sportSegment.getCategoryId())))
                    .flatMap(e -> e.getEvents().stream())
                    .forEach(assetManagementService::setAssetManagementMetaData));
  }

  private TypeSegment setAssetToType(TypeSegment typeSegment, String categoryId) {
    assetManagementService.setAssetForTypeSegment(typeSegment, categoryId);
    return typeSegment;
  }

  /**
   * @param inPlayData : Inplay Data object
   * @param virtualSportDtoCollection : List of all the virtual sports configured in CMS
   */
  private void getVirtualInplayData(
      InPlayData inPlayData, List<VirtualSportDto> virtualSportDtoCollection) {
    Cache cache = cacheManager.getCache(VIRTUAL_SPORT_CACHE);
    List<Event> virtualEvents = null;
    if (cache != null) {
      virtualEvents = cache.get(VIRTUAL_SPORTS, List.class);
    }
    if (virtualEvents == null) {
      log.debug("No virtualEvents data in cache  :" + virtualEvents);
      List<Category> categoriesforVirtualHub = siteServeService.getClassesforVirtualHub();

      List<String> classIds =
          categoriesforVirtualHub.stream()
              .map(cv -> cv.getId().toString())
              .collect(Collectors.toCollection(ArrayList::new));
      virtualEvents = siteServeService.getVirtualEvents(classIds);
    }
    if (CollectionUtils.isEmpty(virtualEvents)) {
      log.debug("Not retrieved virtualEvents data from SS :" + virtualEvents);
      inPlayData.setVirtualSportEvents(new ArrayList<>());
      return;
    }
    log.debug("virtualEvents data  :" + virtualEvents.size());
    Map<String, List<Event>> eventsMap =
        virtualEvents.stream().collect(Collectors.groupingBy(Event::getClassId));

    Map<String, List<VirtualSportDto>> childSportMap =
        virtualSportDtoCollection.stream()
            .flatMap(
                vs ->
                    vs.getTracks().stream()
                        .map(track -> new AbstractMap.SimpleEntry<>(track.getClassId(), vs)))
            .collect(groupingBy(Map.Entry::getKey, mapping(Map.Entry::getValue, toList())));

    eventsMap.keySet().removeIf(c -> !childSportMap.containsKey(c));

    Map<String, Integer> map =
        eventsMap.keySet().stream()
            .map(
                (String key) -> {
                  List<VirtualSportDto> list = childSportMap.get(key);

                  String sportName = list.get(0).getTitle();
                  int liveEventCount = eventsMap.get(key).size();

                  return new VirtualSportEvents(sportName, liveEventCount);
                })
            .collect(
                toMap(
                    VirtualSportEvents::getSportName,
                    VirtualSportEvents::getLiveEventCount,
                    Integer::sum));

    final List<VirtualSportEvents> liveSportList =
        map.keySet().stream()
            .map(key -> new VirtualSportEvents(key, map.get(key)))
            .collect(Collectors.toCollection(ArrayList::new));
    inPlayData.setVirtualSportEvents(liveSportList);
  }

  private InPlayData getInPlayDataEvents(Set<String> categoryIds) {
    List<Category> categories = siteServeService.getClasses(categoryIds);
    Map<String, List<Category>> sportCodeToClassMap =
        categories.stream().collect(groupingBy(Category::getCategoryCode));

    Map<InPlayTopLevelType, List<SportSegment>> sportSegmentsByType =
        sportCodeToClassMap.entrySet().parallelStream()
            .flatMap(
                e -> {
                  String categoryCode = e.getKey();
                  List<Category> classes = e.getValue();
                  return createSportSegment(categoryCode, classes).entrySet().stream();
                })
            .collect(
                groupingBy(
                    Map.Entry::getKey,
                    mapping(Map.Entry::getValue, Collectors.toCollection(ArrayList::new))));

    InPlayModel liveNow = new InPlayModel();
    liveNow
        .getSportEvents()
        .addAll(sportSegmentsByType.getOrDefault(LIVE_EVENT, Collections.emptyList()));

    InPlayModel upcoming = new InPlayModel();
    upcoming
        .getSportEvents()
        .addAll(sportSegmentsByType.getOrDefault(UPCOMING_EVENT, Collections.emptyList()));

    // liveStream is empty so far, will be populated later
    return new InPlayData(liveNow, upcoming, new InPlayModel(), new InPlayModel());
  }

  private Map<InPlayTopLevelType, SportSegment> createSportSegment(
      String categoryCode, List<Category> classes) {
    PrimaryMarkets primaryMarket = PrimaryMarkets.enumerize(categoryCode);
    List<String> classIds =
        classes.stream()
            .map(c -> String.valueOf(c.getId()))
            .collect(Collectors.toCollection(ArrayList::new));
    List<Event> events = siteServeService.getEvents(primaryMarket, classIds);
    List<Event> eventsForPRMarkets =
        primaryMarket != null
            ? siteServeService.getEventsForClassWithPrimaryMarkets(classIds, primaryMarket)
            : events;
    Map<String, Integer> marketCountForEvent;
    if (primaryMarket != null && HR_CATEGORY_CODE.equalsIgnoreCase(primaryMarket.name())) {
      marketCountForEvent = siteServeService.getHRMarketsCountPerEventForClass(classIds);
    } else {
      marketCountForEvent = siteServeService.getMarketsCountPerEventForClass(classIds);
    }
    Map<InPlayTopLevelType, List<Event>> eventsByInPlayType = splitByInplayType(events);
    return transformEntries(
        eventsByInPlayType,
        (type, eventsList) ->
            createSportSegment(type, classes, eventsList, eventsForPRMarkets, marketCountForEvent));
  }

  private SportSegment createSportSegment(
      InPlayTopLevelType eventType,
      List<Category> classes,
      List<Event> events,
      List<Event> eventsForPRMarkets,
      Map<String, Integer> marketCountForEvent) {
    SportSegment sportSegment = new SportSegment();
    classes.stream()
        .findAny()
        .ifPresent(
            category -> {
              sportSegment.setCategoryCode(category.getCategoryCode());
              sportSegment.setCategoryName(category.getCategoryName());
              sportSegment.setDisplayOrder(category.getCategoryDisplayOrder());
              sportSegment.setCategoryId(category.getCategoryId());
              sportSegment.setTopLevelType(eventType);
            });
    sportSegment
        .getEventsByTypeName()
        .addAll(convertToTypeSegments(events, eventsForPRMarkets, marketCountForEvent));

    if (HR_CATEGORY_ID.equals(sportSegment.getCategoryId())) {
      sportSegment.getEventsByTypeName().stream()
          .forEach(typeSegment -> mapToEventModuleData(typeSegment.getEvents()));
    }
    return sportSegment;
  }

  private void mapToEventModuleData(List<EventsModuleData> eventsModuleData) {
    eventsModuleData.stream().forEach(this::mapToEvent);
  }

  private void mapToEvent(EventsModuleData event) {
    Collection<Long> eventIds = new HashSet<>();
    eventIds.add(event.getId());
    Optional<Map<Long, RaceEvent>> raceEventMap =
        dfService.getRaceEvents(Integer.valueOf(event.getCategoryId()), eventIds);
    if (raceEventMap.isPresent()) {
      Map<Long, RaceEvent> racesInfo = raceEventMap.get();
      RaceEvent raceEvent = racesInfo.get(event.getId());
      if (!Objects.nonNull(raceEvent)) return;
      event.setRacingFormEvent(
          getRaceFormEvent(
              raceEvent.getRaceClass(), raceEvent.getDistance(), raceEvent.getGoing()));
      event.getPrimaryMarkets().stream()
          .flatMap(outputMarket -> outputMarket.getOutcomes().stream())
          .forEach(
              outputOutcome ->
                  outputOutcome.setRacingFormOutcome(
                      racingFormOutcome(raceEvent.getHorses(), outputOutcome.getRunnerNumber())));
    }
  }

  private RacingFormEvent getRaceFormEvent(Integer raceClass, String distance, String goingCode) {
    RacingFormEvent formEvent = new RacingFormEvent();
    formEvent.setRaceClass(ObjectUtils.isEmpty(raceClass) ? EMPTY_STRING : raceClass.toString());
    formEvent.setDistance(ObjectUtils.isEmpty(distance) ? EMPTY_STRING : distance);
    formEvent.setGoing(ObjectUtils.isEmpty(goingCode) ? EMPTY_STRING : goingCode);
    return formEvent;
  }

  private OutputRacingFormOutcome racingFormOutcome(List<Horse> horses, Integer runnerNumber) {
    return Objects.nonNull(runnerNumber)
            && isHorsesSizeGreaterThanRunnerNumber(horses.size(), runnerNumber)
        ? getOutputRacingFormOutcome(horses.get(runnerNumber - 1))
        : new OutputRacingFormOutcome();
  }

  private OutputRacingFormOutcome getOutputRacingFormOutcome(Horse horse) {
    if (horse == null) return new OutputRacingFormOutcome();
    OutputRacingFormOutcome racingFormOutcome = new OutputRacingFormOutcome();
    racingFormOutcome.setSilkName(horse.getSilk());
    racingFormOutcome.setDraw(horse.getDraw());
    racingFormOutcome.setTrainer(horse.getTrainer());
    racingFormOutcome.setJockey(horse.getJockey());
    racingFormOutcome.setFormFig(horse.getFormfigs());
    return racingFormOutcome;
  }

  private boolean isHorsesSizeGreaterThanRunnerNumber(int horseSize, Integer runnerNumber) {
    return horseSize > runnerNumber - 1;
  }

  private Map<InPlayTopLevelType, List<Event>> splitByInplayType(List<Event> events) {
    return events.stream()
        .map(this::getInPlayTypeToEventPair)
        .collect(
            groupingBy(
                Pair::getKey, mapping(Pair::getValue, Collectors.toCollection(ArrayList::new))));
  }

  private Pair<InPlayTopLevelType, Event> getInPlayTypeToEventPair(Event event) {
    // In-Play should be defined by attributes is_off = 'Y' and event attribute isStarted
    InPlayTopLevelType eventType =
        isTrue(event.getIsStarted()) && "Y".equals(event.getRawIsOffCode())
            ? LIVE_EVENT
            : UPCOMING_EVENT;
    return Pair.of(eventType, event);
  }

  private InPlayModel getLiveStreamInplayModel(
      InPlayModel source, InPlayTopLevelType topLevelType) {
    InPlayModel newModel = new InPlayModel();
    List<SportSegment> sportSegments =
        getSportEventsWithStream(source.getSportEvents(), topLevelType);
    newModel.getSportEvents().addAll(sportSegments);
    Set<Long> eventIdsWithStream =
        sportSegments.stream().flatMap(sport -> sport.getEventsIds().stream()).collect(toSet());
    newModel.setEventsIds(eventIdsWithStream);
    newModel.setEventCount(eventIdsWithStream.size());
    return newModel;
  }

  private List<SportSegment> getSportEventsWithStream(
      List<SportSegment> sportEvents, InPlayTopLevelType topLevelType) {
    return sportEvents.stream()
        .map(
            sportSegment -> {
              SportSegment newSegment = new SportSegment();
              BeanUtils.copyProperties(sportSegment, newSegment);
              List<TypeSegment> typeSegments =
                  getTypeSegmentWithStream(sportSegment.getEventsByTypeName());
              newSegment.setEventsByTypeName(typeSegments);

              Set<Long> eventIds =
                  typeSegments.stream()
                      .flatMap(type -> type.getEventsIds().stream())
                      .collect(toSet());
              newSegment.setEventsIds(eventIds);
              newSegment.setEventCount(eventIds.size());
              newSegment.setTopLevelType(topLevelType);
              return newSegment;
            })
        .filter(sport -> !sport.getEventsIds().isEmpty())
        .collect(Collectors.toCollection(ArrayList::new));
  }

  private List<TypeSegment> getTypeSegmentWithStream(List<TypeSegment> typeSegments) {
    return typeSegments.stream()
        .map(
            typeSegment -> {
              TypeSegment newTypeSegment = new TypeSegment();
              BeanUtils.copyProperties(typeSegment, newTypeSegment);
              Map<Long, EventsModuleData> eventsWithStream =
                  typeSegment.getEvents().stream()
                      .filter(EventsModuleData::isLiveStreamAvailable)
                      .collect(toMap(EventsModuleData::getId, Function.identity()));
              newTypeSegment.setEvents(new ArrayList<>(eventsWithStream.values()));
              newTypeSegment.setEventsIds(eventsWithStream.keySet());
              newTypeSegment.setEventCount(eventsWithStream.size());
              return newTypeSegment;
            })
        .filter(type -> !type.getEvents().isEmpty())
        .collect(Collectors.toCollection(ArrayList::new));
  }

  private List<TypeSegment> convertToTypeSegments(
      List<Event> eventsList,
      List<Event> eventsForPRMarkets,
      Map<String, Integer> eventMarketCountMap) {

    Map<String, List<OutputMarket>> eventIdToPRMarkets =
        eventsForPRMarkets.parallelStream().collect(toMap(Event::getId, this::getPrimaryMarkets));

    Map<String, List<Event>> eventsGroupByType =
        eventsList.stream().collect(groupingBy(Event::getTypeId));

    return eventsGroupByType.values().stream()
        .map(events -> createTypeSegment(events, eventIdToPRMarkets, eventMarketCountMap))
        .collect(Collectors.toCollection(ArrayList::new));
  }

  private TypeSegment createTypeSegment(
      List<Event> typeEvents,
      Map<String, List<OutputMarket>> eventIdToPRMarkets,
      Map<String, Integer> eventIdToMarketsCount) {
    List<EventsModuleData> eventDatas =
        typeEvents.stream()
            .map(
                event ->
                    toEventsModuleData(
                        event,
                        eventIdToMarketsCount.get(event.getId()),
                        eventIdToPRMarkets.get(event.getId())))
            .collect(Collectors.toCollection(ArrayList::new));
    TypeSegment typeSegment = new TypeSegment();
    typeSegment.getEvents().addAll(eventDatas);
    typeEvents.stream()
        .findAny()
        .ifPresent(
            firstEvent -> {
              typeSegment.setClassName(firstEvent.getClassName());
              typeSegment.setCategoryName(firstEvent.getCategoryName());
              typeSegment.setCategoryCode(firstEvent.getCategoryCode());
              typeSegment.setTypeName(firstEvent.getTypeName());
              typeSegment.setClassDisplayOrder(firstEvent.getClassDisplayOrder());
              typeSegment.setTypeDisplayOrder(firstEvent.getTypeDisplayOrder());
              typeSegment.setTypeId(firstEvent.getTypeId());
            });
    return typeSegment;
  }

  private EventsModuleData toEventsModuleData(
      Event event, Integer marketsCount, List<OutputMarket> primaryMarkets) {
    EventsModuleData item = new EventsModuleData();
    eventMapper.map(item, event);
    item.setMarketsCount(marketsCount);
    item.setPrimaryMarkets(primaryMarkets);
    return item;
  }

  private List<OutputMarket> getPrimaryMarkets(Event event) {
    if (isEmpty(event.getMarkets())) {
      return Collections.emptyList();
    }

    Comparator<OutputMarket> marketComparator = getMarketComparator(event.getCategoryCode());
    return event.getMarkets().parallelStream()
        .map(market -> marketMapper.map(event, market))
        .sorted(marketComparator)
        .collect(Collectors.toCollection(ArrayList::new));
  }

  private Comparator<OutputMarket> getMarketComparator(String categoryCode) {
    PrimaryMarkets primaryMarketsCategory = PrimaryMarkets.enumerize(categoryCode);
    return primaryMarketsCategory != null
        ? comparingInt(
            market ->
                primaryMarketsCategory.getOrderIndex(
                    marketTemplateNameService.getType(market.getName())))
        : comparing(OutputMarket::getTemplateMarketName, this::compareMarketTemplateNames)
            .thenComparing(OutputMarket::getDisplayOrder);
  }

  private int compareMarketTemplateNames(String m1, String m2) {
    if (m1.equals(m2)) {
      return 0;
    }
    if (marketTemplateNameService.containsName(OUTRIGHT, m1)) {
      // outright should be the last one
      return 1;
    }
    // leave markets in as is order
    return -1;
  }
}
