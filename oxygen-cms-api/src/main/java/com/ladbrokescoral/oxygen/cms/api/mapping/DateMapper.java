package com.ladbrokescoral.oxygen.cms.api.mapping;

import java.time.Instant;
import java.time.format.DateTimeFormatter;
import java.time.format.DateTimeFormatterBuilder;
import java.util.Objects;

// FIXME: why do we need custom convertor ?
public class DateMapper {

  private static final DateTimeFormatter MILISEC_FORMATTER =
      new DateTimeFormatterBuilder().appendInstant(3).toFormatter();

  public String toString(Instant date) {
    if (Objects.nonNull(date)) {
      return MILISEC_FORMATTER.format(date);
    }
    return null;
  }
}
