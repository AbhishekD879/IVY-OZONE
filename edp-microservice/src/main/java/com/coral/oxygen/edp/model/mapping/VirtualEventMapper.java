package com.coral.oxygen.edp.model.mapping;

import com.coral.oxygen.edp.model.output.OutputEvent;
import com.egalacoral.spark.siteserver.model.Event;
import java.time.*;
import java.time.format.DateTimeFormatter;
import java.time.temporal.TemporalAccessor;
import lombok.extern.slf4j.Slf4j;

@Slf4j
public class VirtualEventMapper extends ChainedEventMapper {

  public VirtualEventMapper(EventMapper chain) {
    super(chain);
  }

  @Override
  protected void populate(OutputEvent result, Event event) {
    result.setMillisUntilStart(calculateMillisUntilStart(event));
    result.setClassId(event.getClassId());
    result.setClassName(event.getClassName());
  }

  private Long calculateMillisUntilStart(Event event) {
    try {
      TemporalAccessor parsedDateTime =
          DateTimeFormatter.ISO_ZONED_DATE_TIME.parse(event.getStartTime());
      return durationUntilDateFromNow(ZonedDateTime.from(parsedDateTime)).toMillis();
    } catch (DateTimeException | ArithmeticException e) {
      log.error("error in calculating MillisUntilStart", e);
    }
    return null;
  }

  private Duration durationUntilDateFromNow(ZonedDateTime endDateTime) {
    return Duration.between(
        ZonedDateTime.now(Clock.systemUTC()), endDateTime.withZoneSameLocal(ZoneOffset.UTC));
  }
}
