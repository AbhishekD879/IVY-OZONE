package com.coral.oxygen.middleware.featured.service.injector;

import static com.coral.oxygen.middleware.pojos.model.output.MarketTemplateType.WIN_OR_EACH_WAY;
import static java.util.stream.Collectors.toList;
import static java.util.stream.Collectors.toSet;

import com.coral.oxygen.middleware.common.mappers.EventMapper;
import com.coral.oxygen.middleware.common.mappers.RacingForOutcomeMapper;
import com.coral.oxygen.middleware.common.mappers.RacingFormEventMapper;
import com.coral.oxygen.middleware.common.service.MarketTemplateNameService;
import com.coral.oxygen.middleware.common.service.ModuleAdapter;
import com.coral.oxygen.middleware.common.service.featured.IdsCollector;
import com.coral.oxygen.middleware.pojos.model.output.EventsModuleData;
import com.coral.oxygen.middleware.pojos.model.output.OutputMarket;
import com.egalacoral.spark.siteserver.api.BinaryOperation;
import com.egalacoral.spark.siteserver.api.SimpleFilter;
import com.egalacoral.spark.siteserver.api.SimpleFilter.SimpleFilterBuilder;
import com.egalacoral.spark.siteserver.api.SiteServerApi;
import com.egalacoral.spark.siteserver.api.UnaryOperation;
import com.egalacoral.spark.siteserver.model.Children;
import com.egalacoral.spark.siteserver.model.Event;
import com.egalacoral.spark.siteserver.model.RacingFormEvent;
import com.egalacoral.spark.siteserver.model.RacingFormOutcome;
import com.egalacoral.spark.siteserver.parameter.RacingForm;
import java.time.Instant;
import java.util.*;
import java.util.function.Function;
import java.util.stream.Collectors;
import java.util.stream.Stream;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.stereotype.Component;
import org.springframework.util.ObjectUtils;

@Slf4j
@Component
public class RacingEventsModuleInjector extends ModuleAdapter implements EventsModuleInjector {

  private static final String HORSE_RACE_CATEGORY_ID = "21";
  private static final String EVENT = "event";
  private static final String OUTCOME = "outcome";
  private static final String MARKET = "market";

  private final SiteServerApi siteServerApi;
  private final MarketTemplateNameService marketTemplateNameService;
  private final RacingFormEventMapper formEventMapper;
  private final EventMapper eventMapper;
  private final RacingForOutcomeMapper racingForOutcomeMapper;
  private final ConsumeBirHREvents consumeBirHREvents;

  @Autowired
  public RacingEventsModuleInjector(
      @Qualifier("featured") EventMapper eventMapper,
      SiteServerApi siteServerApi,
      RacingForOutcomeMapper racingForOutcomeMapper,
      MarketTemplateNameService marketTemplateNameService,
      RacingFormEventMapper formEventMapper,
      ConsumeBirHREvents consumeBirHREvents) {
    this.siteServerApi = siteServerApi;
    this.eventMapper = eventMapper;
    this.racingForOutcomeMapper = racingForOutcomeMapper;
    this.marketTemplateNameService = marketTemplateNameService;
    this.formEventMapper = formEventMapper;
    this.consumeBirHREvents = consumeBirHREvents;
  }

  public void injectData(List<? extends EventsModuleData> items, IdsCollector idsCollector) {
    Collection<Long> racingEventsIds = new HashSet<>(idsCollector.getRacingEventsIds());
    Collection<Long> selectedByMarketEventIds = getSelectedByMarketRacingEventsIds(items);
    racingEventsIds.addAll(selectedByMarketEventIds);

    List<Children> racingData = consumeHREvents(racingEventsIds);
    List<Children> birData = consumeBirHREvents.consumeBirEvents();
    List<Children> response =
        Stream.concat(racingData.stream(), birData.stream()).toList().stream().distinct().toList();

    Map<String, RacingFormOutcome> racingFormOutcomesMap =
        response.stream()
            .map(Children::getRacingFormOutcome)
            .filter(Objects::nonNull)
            .filter(rfo -> OUTCOME.equalsIgnoreCase(rfo.getRefRecordType()))
            .collect(
                Collectors.toMap(
                    RacingFormOutcome::getRefRecordId, Function.identity(), (a, b) -> a));

    Map<String, RacingFormEvent> racingFormEventMap =
        response.stream()
            .map(Children::getRacingFormEvent)
            .filter(Objects::nonNull)
            .filter(rfo -> EVENT.equalsIgnoreCase(rfo.getRefRecordType()))
            .collect(
                Collectors.toMap(
                    RacingFormEvent::getRefRecordId, Function.identity(), (a, b) -> a));

    Map<String, Event> racingEventsMap =
        response.stream()
            .map(Children::getEvent)
            .filter(Objects::nonNull)
            .collect(Collectors.toMap(Event::getId, Function.identity(), (a, b) -> a));

    items.stream()
        .filter(d -> d.getId() != null)
        .filter(d -> d.getOutcomeId() == null) // only whole events should be processed here
        .filter(
            d ->
                racingEventsMap.containsKey(
                    String.valueOf(d.getId()))) // only whole events should be processed
        // here
        .forEach(
            d -> {
              mapEvent(racingEventsMap, d);
              mapRacingFormEvent(racingFormEventMap, d);
              mapOutcomes(racingFormOutcomesMap, d);
            });

    // events selected by market were already mapped by EventModuleInjector
    // need to exclude marketEvents that do not have corresponding racingEvent that matches required
    // criteria
    clearInvalidRacingMarketEvents(
        items,
        selectedByMarketEventIds.stream()
            .filter(id -> !racingEventsMap.containsKey(String.valueOf(id)))
            .collect(toSet()));
  }

  private void mapOutcomes(
      Map<String, RacingFormOutcome> racingFormOutcomesMap, EventsModuleData d) {
    d.getMarkets().stream()
        .filter(Objects::nonNull)
        .map(OutputMarket::getOutcomes)
        .filter(Objects::nonNull)
        .flatMap(Collection::stream)
        .forEach(
            o -> {
              RacingFormOutcome rfo = racingFormOutcomesMap.get(o.getId());
              if (rfo != null) {
                o.setRacingFormOutcome(racingForOutcomeMapper.map(rfo));
              }
            });
  }

  private void mapEvent(Map<String, Event> racingEventsMap, EventsModuleData d) {
    if (d.getMarketId() == null) {
      // event loaded by market id is not mapped here as it was already mapped by
      // EventModuleInjector
      eventMapper.map(d, racingEventsMap.get(String.valueOf(d.getId())));
    }
  }

  private void mapRacingFormEvent(
      Map<String, RacingFormEvent> racingFormEventMap, EventsModuleData d) {
    RacingFormEvent racingFormEvent = racingFormEventMap.get(String.valueOf(d.getId()));
    if (!ObjectUtils.isEmpty(racingFormEvent)) {
      formEventMapper.map(d, racingFormEvent);
    }
  }

  private void clearInvalidRacingMarketEvents(
      List<? extends EventsModuleData> items, Set<Long> idsToClear) {
    items.removeIf(e -> idsToClear.contains(e.getId()));
  }

  private Collection<Long> getSelectedByMarketRacingEventsIds(
      List<? extends EventsModuleData> items) {
    return items.stream()
        .filter(e -> e.getMarketId() != null && HORSE_RACE_CATEGORY_ID.equals(e.getCategoryId()))
        .map(EventsModuleData::getId)
        .collect(Collectors.toSet());
  }

  private List<Children> consumeHREvents(Collection<Long> eventsIds) {
    SimpleFilter filter =
        (SimpleFilter)
            new SimpleFilterBuilder()
                .addBinaryOperation(
                    "event.suspendAtTime", BinaryOperation.greaterThan, Instant.now())
                .addUnaryOperation("event.isStarted", UnaryOperation.isFalse)
                .addBinaryOperation(
                    "market.templateMarketName",
                    BinaryOperation.intersects,
                    marketTemplateNameService.asQuery(WIN_OR_EACH_WAY))
                .addBinaryOperation("event.eventStatusCode", BinaryOperation.equals, "A")
                .addBinaryOperation("market.marketStatusCode", BinaryOperation.equals, "A")
                .addBinaryOperation("outcome.outcomeStatusCode", BinaryOperation.equals, "A")
                .addBinaryOperation("outcome.outcomeMeaningMinorCode", BinaryOperation.notEquals, 1)
                .addBinaryOperation("outcome.outcomeMeaningMinorCode", BinaryOperation.notEquals, 2)
                .build();

    List<String> prune = new ArrayList<>();
    prune.add(EVENT);
    prune.add(MARKET);

    EnumSet<RacingForm> forms = EnumSet.of(RacingForm.OUTCOME, RacingForm.EVENT);

    List<String> ids = eventsIds.stream().map(Object::toString).collect(toList());
    Optional<List<Children>> data =
        siteServerApi.getEventToOutcomeForEvent(ids, filter, forms, prune);
    return data.orElseGet(ArrayList::new);
  }
}
