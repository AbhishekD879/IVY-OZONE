package com.coral.oxygen.edp.tracking.virtuals;

import com.coral.oxygen.edp.model.mapping.EventMapper;
import com.coral.oxygen.edp.model.output.OutputEvent;
import com.coral.oxygen.edp.model.output.OutputRacingFormOutcome;
import com.coral.oxygen.edp.tracking.QueuedMultiThreadDataConsumer;
import com.coral.oxygen.edp.tracking.model.EventData;
import com.egalacoral.spark.siteserver.api.SiteServerApi;
import com.egalacoral.spark.siteserver.api.SiteServerImpl;
import com.egalacoral.spark.siteserver.model.Children;
import com.egalacoral.spark.siteserver.model.Event;
import com.egalacoral.spark.siteserver.model.RacingFormOutcome;
import com.egalacoral.spark.siteserver.parameter.RacingForm;
import java.util.Collections;
import java.util.EnumSet;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.Set;
import java.util.stream.Collectors;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

@Component
public class VirtualMarketsDataConsumer extends QueuedMultiThreadDataConsumer<Long, EventData> {

  private SiteServerApi siteServerApi;
  private EventMapper eventMapper;

  @Autowired
  public VirtualMarketsDataConsumer(
      SiteServerApi api,
      @Value("${edp.firstmarkets.consumer.queue.size}") int maxQueueSize,
      @Value("${edp.firstmarkets.consumer.thraeds.count}") int threadsCount,
      EventMapper mapper) {
    super(maxQueueSize, threadsCount);
    siteServerApi = api;
    eventMapper = mapper;
  }

  @Override
  protected Map<Long, EventData> doConsume(Set<Long> tickets) {
    List<String> ids = tickets.stream().map(String::valueOf).collect(Collectors.toList());

    Optional<List<Children>> eventWithRacingForm =
        siteServerApi.getEventToOutcomeForEvent(
            ids, SiteServerImpl.EMPTY_SIMPLE_FILTER, EnumSet.of(RacingForm.OUTCOME), null, false);

    List<Children> children = eventWithRacingForm.orElse(Collections.emptyList());

    Map<Long, EventData> result = new HashMap<>();

    Optional.ofNullable(extractEventFromChildren(children))
        .ifPresent(
            event ->
                result.put(
                    getTicket(tickets),
                    new EventData(zipEventWithRacingForms(event, extractRacingForms(children)))));
    return result;
  }

  private long getTicket(Set<Long> tickets) {
    return tickets.stream().findFirst().orElse(0L);
  }

  private OutputEvent zipEventWithRacingForms(Event event, List<RacingFormOutcome> formOutcomes) {
    OutputEvent outputEvent = eventMapper.map(new OutputEvent(), event);

    outputEvent
        .getMarkets()
        .forEach(
            outputMarket ->
                outputMarket
                    .getOutcomes()
                    .forEach(
                        outputOutcome ->
                            outputOutcome.setRacingFormOutcome(
                                getRacingFormForId(formOutcomes, outputOutcome.getId()))));
    return outputEvent;
  }

  private OutputRacingFormOutcome getRacingFormForId(List<RacingFormOutcome> outcomes, String id) {
    return outcomes.stream()
        .filter(racingFormOutcome -> racingFormOutcome.getRefRecordId().equals(id))
        .findFirst()
        .map(OutputRacingFormOutcome::newInstance)
        .orElse(null);
  }

  private List<RacingFormOutcome> extractRacingForms(List<Children> eventWithRacingForm) {
    return eventWithRacingForm.stream()
        .filter(children -> children.getRacingFormOutcome() != null)
        .map(Children::getRacingFormOutcome)
        .collect(Collectors.toList());
  }

  private Event extractEventFromChildren(List<Children> eventWithRacingForm) {
    return eventWithRacingForm.stream()
        .filter(children -> children.getEvent() != null)
        .map(Children::getEvent)
        .findFirst()
        .orElse(null);
  }
}
