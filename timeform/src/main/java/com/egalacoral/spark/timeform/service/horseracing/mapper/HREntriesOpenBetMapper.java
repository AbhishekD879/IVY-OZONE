package com.egalacoral.spark.timeform.service.horseracing.mapper;

import com.egalacoral.spark.siteserver.api.SimpleFilter;
import com.egalacoral.spark.siteserver.api.SiteServerAPI;
import com.egalacoral.spark.siteserver.model.Event;
import com.egalacoral.spark.siteserver.model.Outcome;
import com.egalacoral.spark.timeform.model.horseracing.HREntry;
import com.egalacoral.spark.timeform.model.horseracing.HRMeeting;
import com.egalacoral.spark.timeform.model.horseracing.HRRace;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.stream.Collectors;
import org.apache.commons.lang3.StringUtils;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

@Component
public class HREntriesOpenBetMapper {

  private static final Logger LOGGER = LoggerFactory.getLogger(HREntriesOpenBetMapper.class);

  private SiteServerAPI siteServeAPI;

  @Autowired
  public HREntriesOpenBetMapper(SiteServerAPI siteServeAPI) {
    this.siteServeAPI = siteServeAPI;
  }

  public void mapEntries(Map<HRMeeting, List<HRRace>> map) {
    map.entrySet()
        .forEach(
            entry -> {
              if (entry.getKey().getOpenBetIds() != null
                  && !entry.getKey().getOpenBetIds().isEmpty()) {
                Optional<List<Event>> events = getEventsWithOutcomes(entry.getKey());
                if (events.isPresent()) {
                  mapEntries(entry.getValue(), events.get());
                } else {
                  LOGGER.info(
                      "No open bet events was found for meeting: {}", entry.getKey().getKey());
                  throw new RuntimeException("Can't get events with outcomes from SiteServer API");
                }
              } else {
                LOGGER.info("Meeting: {} has no open bet ids", entry.getKey().getKey());
              }
            });
  }

  private void mapEntries(List<HRRace> races, List<Event> events) {
    races.stream()
        .filter(race -> !race.getEntries().isEmpty())
        .forEach(
            race -> {
              List<Outcome> outcomes =
                  events.stream() //
                      .filter(
                          event ->
                              race.getOpenBetIds().contains(Integer.valueOf(event.getId()))
                                  && event.getMarkets() != null) //
                      .map(event -> event.getMarkets()) //
                      .flatMap(List::stream)
                      .filter(market -> market.getOutcomes() != null) //
                      .map(market -> market.getOutcomes())
                      .flatMap(List::stream)
                      .collect(Collectors.toList());

              race.getEntries()
                  .forEach(
                      entry -> outcomes.forEach(outcome -> mapEntryWithOutcome(entry, outcome)));
            });
  }

  private void mapEntryWithOutcome(HREntry entry, Outcome outcome) {
    String horseName = entry.getHorseName();
    String cleanOutcome = outcome.getName();
    String[] suffixes = {"n/r", "(res)"};
    for (String suffix : suffixes) {
      if (StringUtils.containsIgnoreCase(cleanOutcome, suffix)) {
        cleanOutcome = cleanOutcome.substring(0, cleanOutcome.length() - suffix.length());
      }
      if (StringUtils.containsIgnoreCase(horseName, suffix)) {
        horseName = horseName.substring(0, horseName.length() - suffix.length());
      }
    }
    String pattern = "[^a-zA-Z0-9]+";
    String countryAbrPattern = "(\\([A-Z]+\\))";
    horseName = horseName.replaceAll(countryAbrPattern, "").replaceAll(pattern, "");
    cleanOutcome = cleanOutcome.replaceAll(pattern, "");
    //    LOGGER.debug("Comparing Horse name - {} with Outcome name - {}. Equals - {}",
    // entry.getHorseName(),
    //        outcome.getName(), horseName.equalsIgnoreCase(cleanOutcome));
    if (horseName.equalsIgnoreCase(cleanOutcome)) {
      entry.getOpenBetIds().add(Integer.valueOf(outcome.getId()));
      //      LOGGER.debug("Mapped entry {} to outcome {}", entry, outcome);
    }
  }

  protected Optional<List<Event>> getEventsWithOutcomes(HRMeeting meeting) {
    List<String> typeIds =
        meeting.getOpenBetIds().stream().map(m -> m.toString()).collect(Collectors.toList());
    SimpleFilter.SimpleFilterBuilder builder = new SimpleFilter.SimpleFilterBuilder();
    SimpleFilter build = builder.build();
    Optional<List<Event>> events = siteServeAPI.getEventToOutcomeForType(typeIds, build);
    return events;
  }
}
