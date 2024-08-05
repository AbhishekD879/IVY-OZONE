package com.coral.oxygen.middleware.featured.service.injector;

import com.coral.oxygen.middleware.common.mappers.EventMapper;
import com.coral.oxygen.middleware.common.service.ModuleAdapter;
import com.coral.oxygen.middleware.common.service.featured.IdsCollector;
import com.coral.oxygen.middleware.common.utils.QueryFilterBuilder;
import com.coral.oxygen.middleware.pojos.model.output.EventsModuleData;
import com.coral.oxygen.middleware.pojos.model.output.featured.VirtualEventModule;
import com.egalacoral.spark.siteserver.api.ExistsFilter;
import com.egalacoral.spark.siteserver.api.LimitRecordsFilter;
import com.egalacoral.spark.siteserver.api.LimitToFilter;
import com.egalacoral.spark.siteserver.api.SimpleFilter;
import com.egalacoral.spark.siteserver.api.SiteServerApi;
import com.egalacoral.spark.siteserver.model.Event;
import com.google.common.collect.Lists;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.function.Function;
import java.util.stream.Collectors;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.stereotype.Component;

@Component
@Slf4j
public class VirtualEventDataInjector extends ModuleAdapter implements EventsModuleInjector {

  private static final int PARTITION_SIZE = 50;
  private final SiteServerApi siteServerAPI;
  private final EventMapper eventMapper;
  private final QueryFilterBuilder queryFilterBuilder;

  private final int EVENT_LIMIT = 12;

  @Autowired
  public VirtualEventDataInjector(
      @Qualifier("featured") EventMapper eventMapper,
      SiteServerApi siteServerAPI,
      QueryFilterBuilder queryFilterBuilder) {
    this.siteServerAPI = siteServerAPI;
    this.queryFilterBuilder = queryFilterBuilder;
    this.eventMapper = eventMapper;
  }

  public void injectData(List<? extends EventsModuleData> items, IdsCollector idsCollector) {
    // no need of id's collector variation of method.
  }

  private void mapEvents(List<? extends EventsModuleData> items, Map<String, Event> eventsMap) {
    items.stream()
        .filter(d -> eventsMap.containsKey(String.valueOf(d.getId())))
        .forEach(d -> eventMapper.map(d, eventsMap.get(String.valueOf(d.getId()))));
  }

  public void injectDataEvents(VirtualEventModule module) {
    int limit = module.getLimit() == null ? EVENT_LIMIT : module.getLimit();
    Map<String, Event> eventsMap = getIdEventMap(module.getTypeIds(), limit);
    List<EventsModuleData> items =
        eventsMap.keySet().stream().map(this::toVirtualModule).collect(Collectors.toList());
    mapEvents(items, eventsMap);
    module.setData(items);
  }

  private EventsModuleData toVirtualModule(String s) {

    EventsModuleData module = new EventsModuleData();
    module.setId(Long.valueOf(s));
    return module;
  }

  private Map<String, Event> getIdEventMap(String typeIdString, int limit) {
    List<String> typeIds = Arrays.stream(typeIdString.split(",")).toList();
    List<Event> events = null;
    // bit of pagination if we have type id's more than 100

    events = paginatedSiteServCall(typeIds, limit);

    return events.stream()
        .collect(Collectors.toMap(Event::getId, Function.identity(), (a, b) -> a));
  }

  private List<Event> paginatedSiteServCall(List<String> typeIds, int limit) {

    return Lists.partition(typeIds, PARTITION_SIZE).stream()
        .map(this::consumeEventsByTypeId)
        .flatMap(e -> e.stream())
        .limit(limit)
        .collect(Collectors.toList());
  }

  private List<Event> consumeEventsByTypeId(List<String> typeIds) {
    SimpleFilter simpleFilter = queryFilterBuilder.getFilterForVirtualEvents();
    Optional<List<Event>> virtualEvents = getNextNEventToOutcomeForEvent(typeIds, simpleFilter);

    return virtualEvents.orElse(new ArrayList<>());
  }

  private Optional<List<Event>> getNextNEventToOutcomeForEvent(
      List<String> typeIds, SimpleFilter simpleFilter) {
    return siteServerAPI.getNextNEventToOutcomeForType(
        EVENT_LIMIT,
        typeIds,
        simpleFilter,
        new ExistsFilter.ExistsFilterBuilder().build(),
        new LimitToFilter.LimitToFilterBuilder().build(),
        new LimitRecordsFilter.LimitRecordsFilterBuilder().build(),
        true,
        false);
  }
}
