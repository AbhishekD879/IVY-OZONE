package com.ladbrokescoral.oxygen.notification.utils.time;

import org.joda.time.DateTime;
import org.joda.time.DateTimeZone;
import org.springframework.stereotype.Component;

@Component
public class TimeProviderImpl implements TimeProvider {

  @Override
  public DateTime currentTime() {
    return new DateTime(DateTimeZone.UTC);
  }
}
