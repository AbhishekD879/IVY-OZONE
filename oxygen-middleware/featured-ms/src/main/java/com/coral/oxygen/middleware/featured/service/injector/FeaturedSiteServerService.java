package com.coral.oxygen.middleware.featured.service.injector;

import static com.coral.oxygen.middleware.common.utils.QueryFilterBuilder.*;

import com.coral.oxygen.middleware.common.service.AbstractSiteServeService;
import com.coral.oxygen.middleware.common.service.MarketTemplateNameService;
import com.coral.oxygen.middleware.common.utils.QueryFilterBuilder;
import com.coral.oxygen.middleware.pojos.model.output.MarketTemplateType;
import com.egalacoral.spark.siteserver.api.*;
import com.egalacoral.spark.siteserver.model.Category;
import com.egalacoral.spark.siteserver.model.Children;
import com.egalacoral.spark.siteserver.model.Event;
import com.egalacoral.spark.siteserver.model.Pool;
import java.time.Duration;
import java.util.*;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Component;

@Slf4j
@Component
public class FeaturedSiteServerService extends AbstractSiteServeService {

  public static final String EVENT_EXTERNAL_KEYS_TYPE = "event";

  public FeaturedSiteServerService(
      SiteServerApi siteServerApi, MarketTemplateNameService marketTemplateNameService) {
    super(siteServerApi, marketTemplateNameService);
  }

  public List<Children> getVirtualRacingEventsAndExternalKeys(
      List<String> classIds, String typeFlags, String excludeTypeFlags, Duration startTimeRange) {
    SimpleFilter simpleFilter =
        getRacingEventByTypeFlagsWithStartTimeUntil(
            typeFlags,
            excludeTypeFlags,
            startTimeRange,
            marketTemplateNameService.asQuery(MarketTemplateType.WIN_OR_EACH_WAY));
    ExistsFilter existFilter = getNotSpecialEventsExistFilter();
    List<String> prune = Arrays.asList("event", "market");
    LimitToFilter limitToFilter = getEmptyLimitFilter();
    LimitRecordsFilter limitRecordsFilter = getMarketOutcomesLimitRecordsFilter(1, 1);
    Optional<List<Children>> eventsOptional =
        siteServerApi.getEventToOutcomeForClass(
            classIds,
            simpleFilter,
            limitToFilter,
            limitRecordsFilter,
            existFilter,
            prune,
            EVENT_EXTERNAL_KEYS_TYPE,
            true);
    return eventsOptional.orElse(new ArrayList<>());
  }

  public List<Event> getVirtualRacingEvents(
      List<String> classIds, String raceTypeFlags, String excludeTypeFlags, Duration eventsRange) {
    SimpleFilter simpleFilter =
        getRacingEventByTypeFlagsWithStartTimeUntil(
            raceTypeFlags,
            excludeTypeFlags,
            eventsRange,
            marketTemplateNameService.asQuery(MarketTemplateType.WIN_OR_EACH_WAY));
    ExistsFilter existFilter = getNotSpecialEventsExistFilter();
    List<String> prune = Arrays.asList("event", "market");
    LimitToFilter limitToFilter = getEmptyLimitFilter();
    LimitRecordsFilter limitRecordsFilter = getMarketOutcomesLimitRecordsFilter(1, 1);
    Optional<List<Event>> eventsOptional =
        siteServerApi.getEventToOutcomeForClass(
            classIds, simpleFilter, limitToFilter, limitRecordsFilter, existFilter, prune, true);
    return eventsOptional.orElse(new ArrayList<>());
  }

  public List<Category> getActiveClassesWithOpenEvents(String categoryId) {
    SimpleFilter simpleFilter = getClassWithOpenEventsSimpleFilter(categoryId);
    ExistsFilter existsFilter = getEmptyExistingFilter();
    return siteServerApi.getClasses(simpleFilter, existsFilter).orElse(Collections.emptyList());
  }

  public List<Event> getAllEventToMarketForEvent(List<String> eventIds) {
    return siteServerApi
        .getEventToMarketForEvent(eventIds, Optional.empty(), Optional.empty(), false)
        .orElse(Collections.emptyList());
  }

  public List<Pool> getPoolTypes(List<String> eventIds, List<String> poolTypes) {
    SimpleFilter simpleFilter = getPoolTypesPredicate(poolTypes);
    return siteServerApi
        .getPoolForEvent(String.join(",", eventIds), simpleFilter)
        .orElse(Collections.emptyList());
  }

  public List<Event> getNextRaces(String classId, String excludeTypeIds) {
    return siteServerApi
        .getNextNEventsForClass(
            12,
            Collections.singletonList(classId),
            QueryFilterBuilder.getNextRaces(excludeTypeIds),
            getEmptyExistingFilter(),
            false,
            true)
        .orElse(Collections.emptyList());
  }

  public List<Children> getInternationalToteRacingEventsAndExternalKeys(
      List<String> classIds, Duration eventsSelectionRange) {
    SimpleFilter simpleFilter = getToteEventBySelectionTimeRange(eventsSelectionRange);
    ExistsFilter existFilter = getEmptyExistingFilter();
    List<String> prune = Collections.emptyList();
    LimitToFilter limitToFilter = getEmptyLimitFilter();
    LimitRecordsFilter limitRecordsFilter = getEmptyLimitRecordsFilter();
    Optional<List<Children>> eventsOptional =
        siteServerApi.getEventToOutcomeForClass(
            classIds,
            simpleFilter,
            limitToFilter,
            limitRecordsFilter,
            existFilter,
            prune,
            EVENT_EXTERNAL_KEYS_TYPE,
            true);
    return eventsOptional.orElse(Collections.emptyList());
  }

  public Optional<java.util.List<Event>> getEventToMarketForType(java.util.List<String> marketIds) {
    List<String> prune = Arrays.asList("event");
    return siteServerApi.getEventToMarketForType(marketIds, prune, false);
  }
}
