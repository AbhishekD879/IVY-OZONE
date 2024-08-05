package com.egalacoral.spark.timeform.service.greyhound.mapper;

import com.egalacoral.spark.siteserver.api.SimpleFilter;
import com.egalacoral.spark.siteserver.api.SiteServerAPI;
import com.egalacoral.spark.siteserver.model.Event;
import com.egalacoral.spark.siteserver.model.Market;
import com.egalacoral.spark.siteserver.model.Outcome;
import com.egalacoral.spark.timeform.model.greyhound.Entry;
import com.egalacoral.spark.timeform.model.greyhound.Meeting;
import com.egalacoral.spark.timeform.model.greyhound.Race;
import com.egalacoral.spark.timeform.service.greyhound.MeetingDataMapper;
import java.util.List;
import java.util.Optional;
import java.util.Set;
import java.util.stream.Collectors;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

/** Created by llegkyy on 12.08.16. */
@Component
public class MeetingSelectionMapper implements MeetingDataMapper {

  private SiteServerAPI siteServeAPI;

  private static final Logger LOGGER = LoggerFactory.getLogger(MeetingSelectionMapper.class);

  @Autowired
  public MeetingSelectionMapper(SiteServerAPI siteServeAPI) {
    this.siteServeAPI = siteServeAPI;
  }

  @Override
  public void map(Meeting meeting) {
    SimpleFilter.SimpleFilterBuilder builder = new SimpleFilter.SimpleFilterBuilder();
    SimpleFilter filter = builder.build();
    if (meeting.getOpenBetIds() != null && !meeting.getOpenBetIds().isEmpty()) {
      List<String> meetingIds =
          meeting.getOpenBetIds().stream()
              .map(item -> item.toString())
              .collect(Collectors.toList());
      Optional<List<Event>> events = siteServeAPI.getEventToOutcomeForType(meetingIds, filter);
      if (events.isPresent()) {
        mapEntriesData(meeting, events);
      } else {
        throw new RuntimeException("Can't get events from SiteServer API");
      }
    } else {
      LOGGER.warn(
          "Meeting with id: {} and name: {} hasn't matched open bet type id's",
          meeting.getMeetingId(),
          meeting.getName());
    }
  }

  private void mapEntriesData(Meeting meeting, Optional<List<Event>> events) {
    for (Race race : meeting.getRaces()) {
      Set<Entry> entries = race.getEntries();
      if (events.isPresent()) {
        for (Event event : events.get()) {
          if (race.getOpenBetIds() == null) {
            LOGGER.info("No ObEventIds for Race {}", race.getRaceId());
          }
          List<Market> markets = event.getMarkets();
          if (race.getOpenBetIds() != null
              && race.getOpenBetIds().contains(Integer.valueOf(event.getId()))
              && markets != null
              && entries != null) {
            for (Market market : markets) {
              for (Entry entry : entries) {
                mapEntriesData(entry, market);
              }
            }
          }
        }
      }
    }
  }

  protected void mapEntriesData(Entry entry, Market market) {
    List<Outcome> outcomes = market.getOutcomes();
    if (outcomes == null || outcomes.isEmpty()) {
      LOGGER.info("No outcames found Market {}", market);
    } else {
      for (Outcome outcome : outcomes) {
        mapEntriesData(entry, outcome);
      }
    }
  }

  protected void mapEntriesData(Entry entry, Outcome outcome) {
    String greyHoundFullName =
        entry
            .getGreyHoundFullName()
            .replaceAll("\\s+", "")
            .replaceAll("_", "")
            .replaceAll("-", "")
            .toLowerCase();
    String cleanOutcome =
        outcome
            .getName()
            .replaceAll("\\s+", "")
            .replaceAll("_", "")
            .replaceAll("-", "")
            .toLowerCase();
    String[] sufixes = {"n/r", "(res)"};
    for (String sufix : sufixes) {
      if (cleanOutcome.contains(sufix)) {
        cleanOutcome = cleanOutcome.substring(0, cleanOutcome.length() - sufix.length());
      }
      if (greyHoundFullName.contains(sufix)) {
        greyHoundFullName =
            greyHoundFullName.substring(0, greyHoundFullName.length() - sufix.length());
      }
    }
    LOGGER.debug(
        "Comparing GreyHoundFullName - {} with Outcame fullname - {}. Equals - {}",
        entry.getGreyHoundFullName(),
        cleanOutcome,
        entry.getGreyHoundFullName().equalsIgnoreCase(cleanOutcome));
    if (greyHoundFullName.equalsIgnoreCase(cleanOutcome)) {
      entry.getOpenBetIds().add(Integer.valueOf(outcome.getId()));
      LOGGER.debug("Mapped entry {} to outcome {}", entry, outcome);
    }
  }

  @Override
  public void init() {}
}
