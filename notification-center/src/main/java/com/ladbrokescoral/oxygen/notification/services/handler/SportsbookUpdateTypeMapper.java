package com.ladbrokescoral.oxygen.notification.services.handler;

import static com.ladbrokescoral.oxygen.notification.entities.MessageType.*;

import com.ladbrokescoral.oxygen.notification.entities.sportsbook.Event;
import com.ladbrokescoral.oxygen.notification.entities.sportsbook.Selection;
import com.ladbrokescoral.oxygen.notification.entities.sportsbook.SportsBookEntity;
import com.ladbrokescoral.oxygen.notification.services.ContentConverter;
import com.ladbrokescoral.oxygen.notification.utils.time.TimeProvider;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Objects;
import java.util.stream.Collectors;
import org.joda.time.DateTime;
import org.joda.time.Duration;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

/**
 * Determines the type of update based on message. Simply converts the update json to POJO, and
 * compares its fields.
 */
@Service
public class SportsbookUpdateTypeMapper implements AbstractSportsbookUpdateMapper {

  private ContentConverter contentConverter;
  private final int validTimeFrameMinutes;
  private final TimeProvider timeProvider;

  @Autowired
  public SportsbookUpdateTypeMapper(
      ContentConverter contentConverter,
      @Value("${df.kafka.message.valid_time_frame.minutes}") int timeFrameMinutes,
      TimeProvider timeProvider) {
    this.timeProvider = timeProvider;
    this.validTimeFrameMinutes = timeFrameMinutes;
    this.contentConverter = contentConverter;
  }

  public List<String> forMessage(String message) {
    return contentConverter
        .convert(message)
        .filter(this::isUpdate)
        .filter(this::isWithinValidTimeFrame)
        .map(this::getTypes)
        .orElseGet(Collections::emptyList);
  }

  /** Check if the update message is within last 15 (specified in properties) minutes */
  private boolean isWithinValidTimeFrame(SportsBookEntity entity) {
    DateTime recordModifiedTime = DateTime.parse(entity.getMeta().getRecordModifiedTime());

    return recordModifiedTime.isAfter(
        timeProvider.currentTime().minus(Duration.standardMinutes(validTimeFrameMinutes)));
  }

  private List<String> getTypes(SportsBookEntity entity) {
    List<String> types = new ArrayList<>();

    types.add(goingDown(entity));
    types.add(raceOff(entity));
    types.add(results(entity));
    types.add(nonRunner(entity));
    types.add(streamStarting(entity));

    return types.stream().filter(Objects::nonNull).collect(Collectors.toList());
  }

  private String streamStarting(SportsBookEntity entity) {
    if (getEvent(entity) != null && getEvent(entity).isStreamStarted())
      return STREAM_STARTING.name();

    return null;
  }

  private String goingDown(SportsBookEntity entity) {
    if (getEvent(entity) != null && getEvent(entity).isGoingDown()) return GOING_DOWN.name();

    return null;
  }

  private String raceOff(SportsBookEntity entity) {
    if (getEvent(entity) != null && getEvent(entity).isEventStarted()) return RACE_OFF.name();

    return null;
  }

  private String results(SportsBookEntity entity) {
    if (getEvent(entity) != null && getEvent(entity).isEventResulted()) return RESULTS.name();

    return null;
  }

  private String nonRunner(SportsBookEntity entity) {
    if (getSelection(entity) != null && isNR(getSelection(entity))) return NON_RUNNER.name();

    return null;
  }

  private boolean isNR(Selection selection) {
    return selection.getSelectionName() != null
        && selection.getSelectionName().contains(NON_RUNNER_NAME);
  }

  private Selection getSelection(SportsBookEntity entity) {
    if (entity instanceof Selection) {
      return (Selection) entity;
    }
    return null;
  }

  private Event getEvent(SportsBookEntity entity) {
    if (entity instanceof Event) {
      return (Event) entity;
    }
    return null;
  }
}
