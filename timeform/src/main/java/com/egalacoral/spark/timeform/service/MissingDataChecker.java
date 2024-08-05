package com.egalacoral.spark.timeform.service;

import com.egalacoral.spark.siteserver.api.BinaryOperation;
import com.egalacoral.spark.siteserver.api.SimpleFilter;
import com.egalacoral.spark.siteserver.api.SiteServerAPI;
import com.egalacoral.spark.siteserver.model.Event;
import com.egalacoral.spark.siteserver.model.Type;
import com.egalacoral.spark.timeform.model.LostEvent;
import com.egalacoral.spark.timeform.model.LostOutcome;
import com.egalacoral.spark.timeform.model.MissingTimeFormData;
import com.egalacoral.spark.timeform.model.greyhound.TimeformEntry;
import com.egalacoral.spark.timeform.model.greyhound.TimeformMeeting;
import com.egalacoral.spark.timeform.model.greyhound.TimeformRace;
import com.egalacoral.spark.timeform.service.greyhound.MeetingFilterService;
import com.egalacoral.spark.timeform.service.greyhound.MeetingService;
import com.egalacoral.spark.timeform.tools.Tools;
import java.text.MessageFormat;
import java.text.SimpleDateFormat;
import java.util.*;
import java.util.concurrent.atomic.AtomicReference;
import java.util.function.Consumer;
import java.util.stream.Collectors;
import org.joda.time.DateTime;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

@Component
public class MissingDataChecker {

  private static final String FLAG_CODES_DELIMITER = ",";

  private static final transient Logger LOGGER = LoggerFactory.getLogger(MissingDataChecker.class);

  private static final long leaseLockTime = 1000L * 60 * 3;

  private final SiteServerAPI siteServerAPI;

  private final MeetingService meetingService;

  private final MeetingFilterService meetingFilterService;

  private final MissingDataValidationCalendarService validationCalendarService;

  private final LockService lockService;

  private final String classId;
  // Actually, synchronization/atomicReference is not required here , since data assignment is done
  // in TimeformConfiguration.java i.e one time setting.
  // This will not come under race condition, Even multiple threads work on this bean as setting is
  // done for one time in configuration file.
  // Just gave a fix to remove fortify issue. If this fix is ok , we can go ahead with the other
  // instance variables in this file.
  private AtomicReference<List<Consumer<MissingTimeFormData>>> listeners =
      new AtomicReference<List<Consumer<MissingTimeFormData>>>();

  private Set<String> ignoredTypes = Collections.emptySet();

  private Set<String> ignoredMarkets = Collections.emptySet();

  private Set<String> ignoredSelections = Collections.emptySet();

  private Set<String> ignoredClassFlagCodes = Collections.emptySet();

  private Set<String> ignoredStatusDescriptions = Collections.emptySet();

  @Autowired
  public MissingDataChecker(
      MissingDataValidationCalendarService validationCalendarService,
      LockService lockService,
      SiteServerAPI siteServerAPI,
      MeetingService meetingService,
      MeetingFilterService meetingFilterService,
      @Value("${siteserver.class.id}") String classId) {
    this.validationCalendarService = validationCalendarService;
    this.lockService = lockService;
    this.siteServerAPI = siteServerAPI;
    this.meetingService = meetingService;
    this.meetingFilterService = meetingFilterService;
    this.classId = classId;
  }

  public void validate(Date date) {
    LOGGER.info("Missing data validation for date {}, classid {}", date, classId);
    SimpleDateFormat sdf =
        com.egalacoral.spark.timeform.api.tools.Tools.simpleDateFormat("yyyy-MM-dd");
    String dateStr = sdf.format(date);

    String lockName =
        MessageFormat.format("{0}:{1}:{2}", this.getClass().getSimpleName(), classId, dateStr);

    try {
      lockService.doInLockOrSkip(
          lockName,
          leaseLockTime,
          () -> {
            if (validationCalendarService.isDateValidated(date)) {
              LOGGER.info(
                  "Missing data validation was already performed for date {}, classId {}",
                  date,
                  classId);
              // already validated for this date
              return;
            }

            // get OB types for class
            List<Type> typeForClass =
                siteServerAPI
                    .getClassToSubTypeForClass(
                        classId, new SimpleFilter.SimpleFilterBuilder().build()) //
                    .orElse(new ArrayList<>()) //
                    .stream() //
                    .filter(t -> meetingFilterService.accept(t.getName())) //
                    .filter(t -> !ignoredTypes.contains(t.getName().toLowerCase())) //
                    .collect(Collectors.toList());
            List<String> typeIds =
                typeForClass.stream() //
                    .map(t -> t.getId().toString()) //
                    .collect(Collectors.toList());

            // filter by date
            DateTime dateTime = new DateTime(date);
            SimpleFilter.SimpleFilterBuilder filterBuilder =
                new SimpleFilter.SimpleFilterBuilder() //
                    .addBinaryOperation(
                        "event.startTime",
                        BinaryOperation.greaterThanOrEqual,
                        dateTime.withTime(0, 0, 0, 0))
                    .addBinaryOperation(
                        "event.startTime",
                        BinaryOperation.lessThan,
                        dateTime.plusDays(1).withTime(0, 0, 0, 0));

            Optional<List<Event>> events =
                siteServerAPI.getEventToOutcomeForType(typeIds, filterBuilder.build());
            matchData(date, events.orElse(new ArrayList<>()), typeForClass);

            validationCalendarService.markDateValidated(date);
          });
    } catch (Throwable e) {
      LOGGER.error("Missing data validation failed for classId {} on {}", classId, date, e);
      Thread.currentThread().interrupt();
    }
  }

  private void matchData(Date date, List<Event> eventsFromOB, List<Type> types) {
    Map<String, Type> typesMap =
        types.stream().collect(Collectors.toMap(t -> String.valueOf(t.getId()), Tools.identity()));

    Set<String> typeIdsWithEvents =
        eventsFromOB.stream() //
            .map(Event::getTypeId) //
            .collect(Collectors.toSet());

    // meetings received from timeform
    Collection<? extends TimeformMeeting> meetings = meetingService.getMeetingsByDate(date);

    // ids of meetings received from timeform
    Set<String> meetingIds =
        meetings.stream() //
            .map(TimeformMeeting::getMeetingObEventTypeId) //
            .filter(Objects::nonNull) //
            .flatMap(Set::stream) //
            .filter(Objects::nonNull) //
            .map(Object::toString) //
            .collect(Collectors.toSet());

    // ids of races received from timeform
    Set<String> raceIds =
        meetings.stream() //
            .map(TimeformMeeting::getMeetingRaces) //
            .filter(Objects::nonNull) //
            .flatMap(Set::stream) //
            .filter(Objects::nonNull) //
            .map(TimeformRace::getRaceObEventIds) //
            .filter(Objects::nonNull) //
            .flatMap(Set::stream) //
            .filter(Objects::nonNull) //
            .map(Object::toString) //
            .collect(Collectors.toSet());

    // entries received from timeform
    Set<TimeformEntry> entries =
        meetings.stream() //
            .map(TimeformMeeting::getMeetingRaces) //
            .filter(Objects::nonNull) //
            .flatMap(Set::stream) //
            .filter(Objects::nonNull) //
            .map(TimeformRace::getRaceEntries) //
            .filter(Objects::nonNull) //
            .flatMap(Set::stream) //
            .filter(Objects::nonNull)
            .collect(Collectors.toSet());

    // ids of entries received from timeform
    Set<String> entryIds =
        entries.stream() //
            .filter(Objects::nonNull) //
            .map(TimeformEntry::getObSelectionIds) //
            .filter(Objects::nonNull) //
            .flatMap(Set::stream) //
            .filter(Objects::nonNull) //
            .map(Object::toString) //
            .collect(Collectors.toSet());

    // ignored entries ids
    Set<String> ignoredEntryIds =
        entries.stream() //
            .filter(e -> filterByStatusDescription(e)) //
            .map(TimeformEntry::getObSelectionIds) //
            .filter(Objects::nonNull) //
            .flatMap(Set::stream) //
            .filter(Objects::nonNull) //
            .map(Object::toString) //
            .collect(Collectors.toSet());

    List<LostEvent> lostEvents =
        eventsFromOB.stream() //
            .filter(e -> filterByClassFlagCode(e)) //
            .filter(e -> !raceIds.contains(e.getId())) //
            .map(e -> new LostEvent(typesMap.get(e.getTypeId()), e)) //
            .collect(Collectors.toList());

    // filtering events
    List<Event> notLostEvents =
        eventsFromOB.stream() //
            .filter(e -> raceIds.contains(e.getId())) //
            .collect(Collectors.toList());

    List<LostOutcome> lostOutcomes = new ArrayList<>();

    notLostEvents.stream()
        .filter(e -> filterByClassFlagCode(e)) //
        .forEach(
            e -> {
              e.getMarkets().stream() //
                  .filter(m -> !ignoredMarkets.contains(m.getName().toLowerCase())) //
                  .forEach(
                      m -> {
                        m.getOutcomes().stream() //
                            .filter(o -> !ignoredSelections.contains(o.getName().toLowerCase())) //
                            .filter(o -> !entryIds.contains(o.getId())) //
                            .filter(o -> !ignoredEntryIds.contains(o.getId())) //
                            .forEach(
                                o -> {
                                  lostOutcomes.add(
                                      new LostOutcome(typesMap.get(e.getTypeId()), e, m, o));
                                });
                      });
            });

    List<Type> lostTypes =
        types.stream() //
            .filter(
                t ->
                    !meetingIds.contains(String.valueOf(t.getId())) //
                        && typeIdsWithEvents.contains(String.valueOf(t.getId()))) //
            .collect(Collectors.toList());

    generateAlert(date, lostTypes, lostEvents, lostOutcomes);
  }

  protected boolean filterByClassFlagCode(Event e) {
    LOGGER.info(
        "Filter Event {} codes {} by flag codes {}",
        e.getId(),
        e.getDrilldownTagNames(),
        e.getClassFlagCodes());
    List<String> codes = Collections.emptyList();
    if (e.getDrilldownTagNames() != null) {
      codes = Arrays.asList(e.getDrilldownTagNames().split(FLAG_CODES_DELIMITER));
    }
    return codes.stream().filter(c -> ignoredClassFlagCodes.contains(c.toLowerCase())).count() == 0;
  }

  private boolean filterByStatusDescription(TimeformEntry entry) {
    return (entry.getStatusDescription() != null
        && ignoredStatusDescriptions.contains(entry.getStatusDescription().toLowerCase()));
  }

  private void generateAlert(
      Date date, List<Type> lostTypes, List<LostEvent> lostEvents, List<LostOutcome> lostOutcomes) {
    if (lostTypes.isEmpty() && lostEvents.isEmpty() && lostOutcomes.isEmpty()) {
      LOGGER.info("No missing data found for date {}", date);
      return;
    }
    LOGGER.warn("Missing data found for date {}", date);
    MissingTimeFormData missingTimeFormData =
        new MissingTimeFormData(date, lostTypes, lostEvents, lostOutcomes);
    if (listeners.get() != null) {
      listeners.get().stream().forEach(l -> l.accept(missingTimeFormData));
    }
  }

  public void setListeners(List<Consumer<MissingTimeFormData>> listeners) {
    this.listeners.set(listeners);
  }

  public void setIgnoredTypes(Set<String> ignoredTypes) {
    this.ignoredTypes = ignoredTypes.stream().map(String::toLowerCase).collect(Collectors.toSet());
  }

  public void setIgnoredMarkets(Set<String> ignoredMarkets) {
    this.ignoredMarkets =
        ignoredMarkets.stream().map(String::toLowerCase).collect(Collectors.toSet());
  }

  public void setIgnoredSelections(Set<String> ignoredSelections) {
    this.ignoredSelections =
        ignoredSelections.stream().map(String::toLowerCase).collect(Collectors.toSet());
  }

  public void setIgnoredClassFlagCodes(Set<String> ignoredEventFalgs) {
    this.ignoredClassFlagCodes =
        ignoredEventFalgs.stream().map(String::toLowerCase).collect(Collectors.toSet());
  }

  public void setIgnoredStatusDescriptions(Set<String> ignoredStatusDescriptions) {
    this.ignoredStatusDescriptions =
        ignoredStatusDescriptions.stream().map(String::toLowerCase).collect(Collectors.toSet());
  }
}
