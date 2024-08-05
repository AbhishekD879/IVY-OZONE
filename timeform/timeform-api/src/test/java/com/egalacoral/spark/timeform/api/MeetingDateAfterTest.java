package com.egalacoral.spark.timeform.api;

import com.egalacoral.spark.timeform.api.services.endpoints.params.MeetingDateAfter;
import java.util.Calendar;
import java.util.Date;
import org.junit.Assert;
import org.junit.Ignore;
import org.junit.Test;

public class MeetingDateAfterTest {

  @Ignore
  @Test
  public void meetingDateAfter() {
    Date date = new Calendar.Builder().setDate(2000, 1, 1).build().getTime();
    MeetingDateAfter eq = new MeetingDateAfter("performances/", date);
    Assert.assertEquals("performances/meeting_date gt datetime'2000-01-31'", eq.build());
  }
}
