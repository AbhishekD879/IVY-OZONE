package com.egalacoral.spark.timeform.service.horseracing.mapper;

import com.egalacoral.spark.siteserver.api.SimpleFilter;
import com.egalacoral.spark.siteserver.api.SiteServerAPI;
import com.egalacoral.spark.siteserver.model.Event;
import com.egalacoral.spark.timeform.model.horseracing.HRMeeting;
import com.egalacoral.spark.timeform.model.horseracing.HRRace;
import java.time.LocalDateTime;
import java.time.ZoneId;
import java.util.*;
import java.util.stream.Collectors;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

@Component
public class HRRacesOpenBetMapper {

  private static final Logger LOGGER = LoggerFactory.getLogger(HRRacesOpenBetMapper.class);
  private final String INVALID_START_TIME_GMT_SCHEDULED = "1990-01-01T00:00:00.000";

  private SiteServerAPI siteServeAPI;

  @Autowired
  public HRRacesOpenBetMapper(SiteServerAPI siteServeAPI) {
    this.siteServeAPI = siteServeAPI;
  }

  public void mapRaces(Map<HRMeeting, List<HRRace>> map) {
    map.entrySet()
        .forEach(
            entry -> {
              if (entry.getKey().getOpenBetIds() != null
                  && !entry.getKey().getOpenBetIds().isEmpty()) {
                Optional<List<Event>> events = getEvents(entry.getKey());
                if (events.isPresent()) {
                  mapRaces(entry.getValue(), events.get());
                } else {
                  LOGGER.info(
                      "No open bet events was found for meeting: {}", entry.getKey().getKey());
                  throw new RuntimeException("Can't get events from SiteServer API");
                }
              } else {
                LOGGER.info("Meeting: {} has no open bet ids", entry.getKey().getKey());
              }
            });
  }

  private void mapRaces(List<HRRace> races, List<Event> events) {
    events.forEach(
        event ->
            races.forEach(
                race -> {
                  if (!INVALID_START_TIME_GMT_SCHEDULED.equals(race.getStartTimeGMTScheduled())) {
                    if (compareDate(race, event)) {
                      race.getOpenBetIds().add(Integer.valueOf(event.getId()));
                    }
                  } else {
                    LOGGER.info(
                        "Race {} start time {} is invalid",
                        race.getKey(),
                        race.getStartTimeGMTScheduled());
                  }
                }));
  }

  private boolean compareDate(HRRace race, Event event) {
    LocalDateTime raceDate = LocalDateTime.parse(race.getStartTimeGMTScheduled());
    raceDate = raceDate.atZone(ZoneId.of("Europe/London")).toLocalDateTime();
    LocalDateTime eventDate = LocalDateTime.parse(event.getStartTime().replace("Z", ""));
    LOGGER.debug("RaceDate - {}, EventDate - {}", raceDate, eventDate);
    return raceDate.isEqual(eventDate);
  }

  protected Optional<List<Event>> getEvents(HRMeeting meeting) {
    if (meeting.getOpenBetIds().isEmpty()) {
      return Optional.of(new ArrayList<>());
    }
    List<String> typeIds =
        meeting.getOpenBetIds().stream().map(m -> m.toString()).collect(Collectors.toList());
    SimpleFilter.SimpleFilterBuilder builder = new SimpleFilter.SimpleFilterBuilder();
    SimpleFilter build = builder.build();
    Optional<List<Event>> events = siteServeAPI.getEventForType(typeIds, build);
    return events;
  }
}
