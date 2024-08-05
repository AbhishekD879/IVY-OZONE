package com.egalacoral.spark.timeform.controller.api;

import com.egalacoral.spark.timeform.model.greyhound.Meeting;
import com.egalacoral.spark.timeform.service.greyhound.TimeformMeetingService;
import io.swagger.annotations.ApiParam;
import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.PathVariable;

@javax.annotation.Generated(
    value = "class io.swagger.codegen.languages.SpringCodegen",
    date = "2016-09-02T07:48:35.998Z")
@Controller
public class GrayhoundRacesMeetingApiController implements GrayhoundRacesMeetingApi {

  @Autowired private TimeformMeetingService service;

  @Override
  public ResponseEntity<Meeting> meetingMeetingIdGet(
      @ApiParam(value = "ID of the meeting", required = true) @PathVariable("meetingId")
          Integer meetingId) {
    return ResponseEntityBuilder.build(service.getMeeting(meetingId));
  }

  @Override
  public ResponseEntity<List<Meeting>> meetingOpenbetIdOpenbetGet(
      @ApiParam(value = "Comma separated list of OpenBet ID of the meeting", required = true)
          @PathVariable("openbetId")
          List<Integer> openbetId) {
    return ResponseEntityBuilder.build(service.getMeetingByOpenbetId(openbetId));
  }
}
