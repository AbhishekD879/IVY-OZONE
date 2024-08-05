package com.coral.oxygen.edp.tracking.firstmarkets;

import com.coral.oxygen.edp.model.mapping.EventMapper;
import com.coral.oxygen.edp.model.output.OutputEvent;
import com.coral.oxygen.edp.model.output.OutputRacingFormOutcome;
import com.coral.oxygen.edp.service.DfApiService;
import com.coral.oxygen.edp.tracking.QueuedMultiThreadDataConsumer;
import com.coral.oxygen.edp.tracking.model.FirstMarketsData;
import com.coral.oxygen.edp.tracking.model.HorseDTO;
import com.coral.oxygen.edp.tracking.model.RaceDTO;
import com.egalacoral.spark.siteserver.api.BinaryOperation;
import com.egalacoral.spark.siteserver.api.SimpleFilter;
import com.egalacoral.spark.siteserver.api.SiteServerApi;
import com.egalacoral.spark.siteserver.api.SiteServerException;
import com.egalacoral.spark.siteserver.model.Children;
import com.egalacoral.spark.siteserver.model.Event;
import java.io.IOException;
import java.util.*;
import java.util.stream.Collectors;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;
import org.springframework.util.ObjectUtils;

/** Created by azayats on 22.12.17. */
@Component
@Slf4j
public class FirstmarketsDataConsumer
    extends QueuedMultiThreadDataConsumer<Long, FirstMarketsData> {

  private final SiteServerApi siteServerApi;
  private final EventMapper eventMapper;
  private final DfApiService dfApiService;
  public static final int CATEGORYID = 21;

  @Autowired
  public FirstmarketsDataConsumer(
      SiteServerApi siteServerApi, //
      @Value("${edp.firstmarkets.consumer.queue.size}") int queueSize, //
      @Value("${edp.firstmarkets.consumer.thraeds.count}") int threadsCount, //
      EventMapper eventMapper, //
      DfApiService dfApiService) {
    super(queueSize, threadsCount);
    this.siteServerApi = siteServerApi;
    this.eventMapper = eventMapper;
    this.dfApiService = dfApiService;
  }

  @Override
  protected Map<Long, FirstMarketsData> doConsume(Set<Long> tickets) {
    Map<Long, FirstMarketsData> result = null;
    try {
      List<String> ids =
          tickets.stream().map(String::valueOf).collect(Collectors.toCollection(ArrayList::new));
      SimpleFilter simpleFilter =
          (SimpleFilter)
              new SimpleFilter.SimpleFilterBuilder()
                  .addBinaryOperation("event.siteChannels", BinaryOperation.contains, "M")
                  .addBinaryOperation("market.siteChannels", BinaryOperation.contains, "M")
                  .addField("market.isMarketBetInRun")
                  .addField("market.isDisplayed")
                  .build();
      Optional<List<Children>> eventToOutcomeForEvent =
          siteServerApi.getEventToOutcomeForEvent(ids, simpleFilter, null, Collections.emptyList());

      Map<Long, RaceDTO> races =
          dfApiService.getNextRaces(CATEGORYID, tickets).orElse(new HashMap<>());

      if (eventToOutcomeForEvent.isPresent()) {
        result =
            eventToOutcomeForEvent.get().stream()
                .map(Children::getEvent)
                .filter(Objects::nonNull)
                .map(event -> mapToEvent(event, races))
                .collect(
                    Collectors.toMap(
                        eventKey -> Long.parseLong(eventKey.getId().toString()),
                        eventValue -> {
                          FirstMarketsData data = new FirstMarketsData();
                          log.info("FirstmarketsDataConsumer eventValue {}", eventValue);
                          data.setEvent(eventValue);
                          return data;
                        }));

        result.values().forEach(FirstMarketsData::populateCache);

      } else {
        throw new SiteServerException("Error consuming data from siteserver for ids " + tickets);
      }
    } catch (IOException ie) {
      log.error("error while fetching df data ", ie);
    }
    return result;
  }

  private OutputEvent mapToEvent(Event event, Map<Long, RaceDTO> races) {
    OutputEvent outputEvent = eventMapper.map(new OutputEvent(), event);
    Optional<RaceDTO> raceDTO = Optional.ofNullable(races.get(Long.parseLong(event.getId())));
    log.info("mapToEvent raceDTO {} ", raceDTO.toString());
    if (!raceDTO.isPresent()) return outputEvent;

    outputEvent.getMarkets().stream()
        .flatMap(outputMarket -> outputMarket.getOutcomes().stream())
        .forEach(
            outputOutcome ->
                outputOutcome.setRacingFormOutcome(
                    newRacingFormForId(
                        raceDTO.get().getHorses(), outputOutcome.getRunnerNumber())));
    return outputEvent;
  }

  private OutputRacingFormOutcome newRacingFormForId(List<HorseDTO> horses, Integer runnerNumber) {
    return !ObjectUtils.isEmpty(runnerNumber)
            && isHorsesSizeGreaterThanRunnerNumber(horses.size(), runnerNumber)
        ? getOutputRacingFormOutcome(horses.get(runnerNumber - 1))
        : new OutputRacingFormOutcome();
  }

  private boolean isHorsesSizeGreaterThanRunnerNumber(int horseSize, Integer runnerNumber) {
    return horseSize > runnerNumber - 1;
  }

  private OutputRacingFormOutcome getOutputRacingFormOutcome(HorseDTO horseDTO) {
    if (horseDTO == null) return new OutputRacingFormOutcome();
    return OutputRacingFormOutcome.builder()
        .age(horseDTO.getHorseAge().toString())
        .trainer(horseDTO.getTrainer())
        .jockey(horseDTO.getJockey())
        .owner(horseDTO.getOwner())
        .silkName(horseDTO.getSilk())
        .weight(horseDTO.getWeight())
        .draw(horseDTO.getDraw())
        .build();
  }
}
