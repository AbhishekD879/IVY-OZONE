package com.egalacoral.spark.timeform.api.services.endpoints.params;

public class MeetingId extends FilterParamValue<Integer> {

  private MeetingId(String template, Integer value) {
    super(template, value);
  }

  public static MeetingId eq(Integer value) {
    return new MeetingId("meeting_id eq %s", value);
  }

}
