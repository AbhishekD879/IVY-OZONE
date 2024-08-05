package com.egalacoral.spark.timeform.service.greyhound.mapper;

import com.egalacoral.spark.siteserver.api.SimpleFilter;
import com.egalacoral.spark.siteserver.api.SiteServerAPI;
import com.egalacoral.spark.siteserver.model.Event;
import com.egalacoral.spark.timeform.model.greyhound.Meeting;
import com.egalacoral.spark.timeform.model.greyhound.Race;
import com.egalacoral.spark.timeform.service.greyhound.MeetingDataMapper;
import java.text.ParseException;
import java.util.*;
import java.util.stream.Collectors;
import org.joda.time.LocalDateTime;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.util.Assert;

public class MeetingOpenBetIdMapper implements MeetingDataMapper {

  private SiteServerAPI siteServeAPI;

  private static final Logger LOGGER = LoggerFactory.getLogger(MeetingOpenBetIdMapper.class);

  public MeetingOpenBetIdMapper(SiteServerAPI siteServeAPI) {
    this.siteServeAPI = siteServeAPI;
  }

  @Override
  public void map(Meeting meeting) {
    if (meeting.getOpenBetIds() != null) {
      Optional<List<Event>> eventsOptional = getEvents(meeting);
      if (eventsOptional.isPresent()) {
        mapMeeting(meeting, eventsOptional);
      } else {
        LOGGER.error("Can't find events for open bet type id {}", meeting.getOpenBetIds());
        throw new RuntimeException("Can't get events from SiteServer API");
      }
    }
  }

  protected void mapMeeting(Meeting meeting, Optional<List<Event>> eventsOptional) {
    if (eventsOptional.isPresent()) {
      List<Event> events = eventsOptional.get();
      Set<Race> races = meeting.getRaces();
      if (races != null) {
        for (Race race : races) {
          map(race, events);
          if (race.getOpenBetIds() == null || race.getOpenBetIds().isEmpty()) {
            LOGGER.debug("Can't map ob event id for race {} with {}", race, events);
          }
        }
      } else {
        LOGGER.error("Can't find races for meeting {}", meeting);
      }
    }
  }

  protected void map(Race race, List<Event> events) {
    mapMeeting(race, events);
  }

  protected Optional<List<Event>> getEvents(Meeting meeting) {
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

  private void mapMeeting(Race race, List<Event> list) {
    Assert.notNull(
        race.getScheduledRaceTimeGmt(), "Race scheduled race time local must be not null");
    for (Event event : list) {
      mapRace(race, event);
    }
  }

  protected void mapRace(Race race, Event event) {
    try {
      mapRaceData(race, event);
    } catch (ParseException e) {
      LOGGER.error("Can't parse schedule local time for event {}", event, e);
    }
  }

  protected void mapRaceData(Race race, Event event) throws ParseException {
    LocalDateTime raceDate = LocalDateTime.parse(race.getScheduledRaceTimeGmt());
    LocalDateTime eventDate = LocalDateTime.parse(event.getStartTime().replace("Z", ""));
    LOGGER.debug("RaceDate - {}, EventDate - {}", raceDate, eventDate);
    if (raceDate.equals(eventDate)) {
      if (race.getOpenBetIds() == null) {
        race.setOpenBetIds(new HashSet<>());
      }
      race.getOpenBetIds().add(Integer.valueOf(event.id));
      LOGGER.debug("Mapped event {} to race {}", event, race);
    }
  }

  @Override
  public void init() {
    // do nothing
  }
}
