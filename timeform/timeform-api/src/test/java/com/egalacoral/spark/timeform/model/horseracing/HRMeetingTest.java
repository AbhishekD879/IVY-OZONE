package com.egalacoral.spark.timeform.model.horseracing;

import com.google.gson.Gson;
import org.junit.Assert;
import org.junit.Test;

public class HRMeetingTest {

  @Test
  public void testMeetingDate() {
    Gson gson = new Gson();

    String str =
        "{\n"
            + "      \"meetingDate\": \"1901-09-02T00:00:00\",\n"
            + "      \"courseId\": 1,\n"
            + "      \"courseName\": \"ASCOT\",\n"
            + "      \"meetingSurfaceName\": \"Turf\",\n"
            + "      \"meetingSurfaceChar\": \"T\",\n"
            + "      \"meetingStatus\": \"To Take Place\",\n"
            + "      \"meetingRaceType\": \"Flat\",\n"
            + "      \"meetingNumberSuffix\": \"OOO\",\n"
            + "      \"meetingNumber\": 554,\n"
            + "      \"inspectionTime\": \"1900-01-01T00:00:00\",\n"
            + "      \"meetingGoing\": \"Good (Good to Firm in places)\",\n"
            + "      \"publishFlag\": 3\n"
            + "    }";

    HRMeeting meeting = gson.fromJson(str, HRMeeting.class);
    Assert.assertEquals("1901-09-02T00:00:00", meeting.getMeetingDate());
    Assert.assertEquals(Integer.valueOf(1), meeting.getCourseId());
    Assert.assertEquals("ASCOT", meeting.getCourseName());
    Assert.assertEquals("Turf", meeting.getMeetingSurfaceName());
    Assert.assertEquals("T", meeting.getMeetingSurfaceChar());
    Assert.assertEquals("To Take Place", meeting.getMeetingStatus());
    Assert.assertEquals("Flat", meeting.getMeetingRaceType());
    Assert.assertEquals("OOO", meeting.getMeetingNumberSuffix());
    Assert.assertEquals(Integer.valueOf(554), meeting.getMeetingNumber());
    Assert.assertEquals("1900-01-01T00:00:00", meeting.getInspectionTime());
    Assert.assertEquals("Good (Good to Firm in places)", meeting.getMeetingGoing());
    Assert.assertEquals(Integer.valueOf(3), meeting.getPublishFlag());
  }
}
