package com.coral.oxygen.middleware.featured.consumer.sportpage.racing;

import com.coral.oxygen.middleware.common.mappers.ExternalKeyMapper;
import com.coral.oxygen.middleware.common.mappers.RacingModuleDataMapper;
import com.coral.oxygen.middleware.common.mappers.SiteServeChildrenMapper;
import com.coral.oxygen.middleware.featured.consumer.sportpage.RacingModuleType;
import com.coral.oxygen.middleware.featured.service.injector.ConsumeBirHREvents;
import com.coral.oxygen.middleware.featured.service.injector.FeaturedSiteServerService;
import com.coral.oxygen.middleware.pojos.model.cms.featured.CmsRacingModule;
import com.coral.oxygen.middleware.pojos.model.cms.featured.RacingConfig;
import com.coral.oxygen.middleware.pojos.model.cms.featured.SportModule;
import com.coral.oxygen.middleware.pojos.model.output.RacingEventData;
import com.coral.oxygen.middleware.pojos.model.output.featured.RacingEventsModule;
import com.egalacoral.spark.siteserver.model.Category;
import com.egalacoral.spark.siteserver.model.Children;
import com.egalacoral.spark.siteserver.model.Event;
import com.egalacoral.spark.siteserver.model.ExternalKeys;
import com.egalacoral.spark.siteserver.model.Market;
import com.egalacoral.spark.siteserver.model.Pool;
import java.time.Duration;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collection;
import java.util.Collections;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.Set;
import java.util.regex.Pattern;
import java.util.stream.Collectors;
import java.util.stream.Stream;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.util.CollectionUtils;

@Slf4j
@Service
@RequiredArgsConstructor
public class RacingEventModuleService
    extends AbstractRacingModuleService<RacingEventData, RacingEventsModule> {

  private static final Pattern EXTERNAL_KEY_TYPE_CODES_PATTERN =
      Pattern.compile("(?i)(OBEvLinkTote|OBEvLinkScoop6|OBEvLinkPlacepot7)");

  private static final List<String> SUPPORTED_POOL_TYPES =
      Arrays.asList("UPLP", "UQDP", "UJKP", "USC6", "UPP7");

  private static final int EVENTS_SELECTION_DAYS = 3;

  private final FeaturedSiteServerService siteServerService;
  private final RacingModuleDataMapper racingEventMapper;
  private final ExternalKeyMapper externalKeysMapper;
  private final SiteServeChildrenMapper childrenMapper;
  private final ConsumeBirHREvents consumeBirHREvents;

  @Override
  protected RacingEventsModule createModule(
      SportModule cmsModule, RacingModuleType racingModuleType, boolean active) {
    return new RacingEventsModule(cmsModule, racingModuleType.getAbbreviation(), active);
  }

  @Override
  protected List<RacingEventData> getData(
      SportModule cmsModule,
      List<CmsRacingModule> racingConfigs,
      RacingModuleType racingModuleType) {
    return getRacingEvents(cmsModule.getSportId(), racingConfigs, racingModuleType);
  }

  private List<RacingEventData> getRacingEvents(
      Integer sportId, List<CmsRacingModule> racingConfigs, RacingModuleType raceType) {
    List<Event> events;
    Map<String, Set<String>> eventPools;

    List<String> classes = getActiveClasses(sportId);
    Duration eventsSelectionRange = Duration.ofDays(getMaxEventSelectionDays(racingConfigs));
    if (isTotePoolIndicatorsEnabled(racingConfigs)) {
      List<Children> eventsAndExternalKeys =
          getEventsAndExternalKeys(classes, raceType, eventsSelectionRange);
      events = childrenMapper.map(eventsAndExternalKeys, Children::getEvent);
      Map<String, List<String>> eventToExternalEventIds =
          getEventToExternalKeysIds(
              childrenMapper.map(eventsAndExternalKeys, Children::getExternalKeys));
      eventPools = getExternalEventsPoolTypes(eventToExternalEventIds);
    } else {
      events = getEvents(raceType, classes, eventsSelectionRange);
      List<Children> birData = consumeBirHREvents.consumeBirEvents();
      List<Event> birEvents = childrenMapper.map(birData, Children::getEvent);
      log.info("getRacingEvents BirEvents {}", birEvents);
      events =
          Stream.concat(birEvents.stream(), events.stream()).toList().stream().distinct().toList();
      eventPools = Collections.emptyMap();
    }
    return events.stream()
        .filter(e -> raceType == RacingModuleType.getTypeByFlags(e.getTypeFlagCodes()))
        .filter(this::hasMarketWithOutcome)
        .map(e -> toRacingData(e, eventPools))
        .collect(Collectors.toCollection(ArrayList::new));
  }

  private int getMaxEventSelectionDays(List<CmsRacingModule> racingConfigs) {
    return racingConfigs.stream()
        .map(CmsRacingModule::getRacingConfig)
        .mapToInt(RacingConfig::getEventsSelectionDays)
        .max()
        .orElse(EVENTS_SELECTION_DAYS);
  }

  private RacingEventData toRacingData(Event event, Map<String, Set<String>> eventPools) {
    return racingEventMapper.mapRacingEventData(
        event, new ArrayList<>(eventPools.getOrDefault(event.getId(), Collections.emptySet())));
  }

  private List<Event> getEvents(
      RacingModuleType raceType, List<String> classes, Duration eventsStartRange) {
    return siteServerService.getVirtualRacingEvents(
        classes, raceType.getTypeFlags(), raceType.getExcludeTypeFlags(), eventsStartRange);
  }

  private List<Children> getEventsAndExternalKeys(
      List<String> classes, RacingModuleType raceType, Duration eventsStartRange) {
    return siteServerService.getVirtualRacingEventsAndExternalKeys(
        classes, raceType.getTypeFlags(), raceType.getExcludeTypeFlags(), eventsStartRange);
  }

  private boolean hasMarketWithOutcome(Event racingEvent) {
    return !CollectionUtils.isEmpty(racingEvent.getMarkets())
        && racingEvent.getMarkets().stream()
            .anyMatch(m -> !CollectionUtils.isEmpty(m.getOutcomes()));
  }

  private List<String> getActiveClasses(Integer sportId) {
    List<Category> classes = siteServerService.getActiveClassesWithOpenEvents(sportId.toString());
    return classes.stream()
        .map(Category::getId)
        .map(Object::toString)
        .collect(Collectors.toCollection(ArrayList::new));
  }

  private boolean isTotePoolIndicatorsEnabled(List<CmsRacingModule> racingConfigs) {
    return racingConfigs.stream()
        .map(CmsRacingModule::getRacingConfig)
        .anyMatch(RacingConfig::isEnablePoolIndicators);
  }

  private Map<String, List<String>> getEventMarketsMap(List<String> eventIds) {
    return siteServerService.getAllEventToMarketForEvent(eventIds).stream()
        .collect(
            Collectors.toMap(
                Event::getId,
                e ->
                    e.getMarkets().stream()
                        .map(Market::getId)
                        .collect(Collectors.toCollection(ArrayList::new))));
  }

  private Map<String, Set<String>> getExternalEventsPoolTypes(
      Map<String, List<String>> eventToExternalEventIds) {
    if (eventToExternalEventIds.isEmpty()) {
      return Collections.emptyMap();
    }
    List<String> externalEvents =
        eventToExternalEventIds.values().stream()
            .flatMap(Collection::stream)
            .distinct()
            .collect(Collectors.toCollection(ArrayList::new));
    List<Pool> poolTypes = siteServerService.getPoolTypes(externalEvents, SUPPORTED_POOL_TYPES);
    if (poolTypes.isEmpty()) {
      return Collections.emptyMap();
    }
    Map<String, List<String>> externalEventMarkets = getEventMarketsMap(externalEvents);
    Map<String, Set<String>> marketPoolTypes = getMarketPoolTypes(poolTypes);
    return eventToExternalEventIds.entrySet().stream()
        .collect(
            Collectors.toMap(
                Map.Entry::getKey,
                e ->
                    getPoolTypes(
                        getMarketIds(e.getValue(), externalEventMarkets), marketPoolTypes)));
  }

  private List<String> getMarketIds(
      List<String> externalEventIds, Map<String, List<String>> externalEventMarkets) {
    return externalEventIds.stream()
        .flatMap(
            externalEventId ->
                externalEventMarkets
                    .getOrDefault(externalEventId, Collections.emptyList())
                    .stream())
        .collect(Collectors.toCollection(ArrayList::new));
  }

  private Map<String, Set<String>> getMarketPoolTypes(List<Pool> poolTypes) {
    Map<String, Set<String>> marketPoolTypes = new HashMap<>();
    poolTypes.forEach(
        (Pool pool) -> {
          List<String> marketIds =
              Optional.ofNullable(pool.getMarketIds())
                  .map(m -> Arrays.asList(m.split(",")))
                  .orElse(Collections.emptyList());
          marketIds.forEach(
              id -> marketPoolTypes.computeIfAbsent(id, k -> new HashSet<>()).add(pool.getType()));
        });
    return marketPoolTypes;
  }

  private Set<String> getPoolTypes(
      List<String> marketIds, Map<String, Set<String>> marketsToPoolTypes) {
    return marketIds.stream()
        .flatMap(m -> marketsToPoolTypes.getOrDefault(m, Collections.emptySet()).stream())
        .collect(Collectors.toSet());
  }

  public Map<String, List<String>> getEventToExternalKeysIds(List<ExternalKeys> externalKeys) {
    return externalKeys.stream()
        .filter(k -> EXTERNAL_KEY_TYPE_CODES_PATTERN.matcher(k.getExternalKeyTypeCode()).matches())
        .flatMap(k -> externalKeysMapper.mapToEventIds(k).entrySet().stream())
        .collect(
            Collectors.toMap(
                Map.Entry::getKey,
                entry -> new ArrayList<>(Arrays.asList(entry.getValue())),
                (List<String> v1, List<String> v2) -> {
                  v1.addAll(v2);
                  return v1;
                }));
  }
}
