package com.egalacoral.spark.timeform.controller.api;

import com.egalacoral.spark.timeform.model.horseracing.HRMeeting;
import com.egalacoral.spark.timeform.service.horseracing.HorseRacingStorageService;
import com.egalacoral.spark.timeform.timer.Timer;
import io.swagger.annotations.ApiParam;
import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.PathVariable;

@javax.annotation.Generated(
    value = "class io.swagger.codegen.languages.SpringCodegen",
    date = "2016-09-19T14:33:52.182Z")
@Controller
public class HorseRacesMeetingApiController implements HorseRacesMeetingApi {

  @Autowired private HorseRacingStorageService service;

  @Timer
  public ResponseEntity<List<HRMeeting>> meetingOpenbetIdGet(
      @ApiParam(value = "Comma separated list of OpenBet ID of the meeting", required = true)
          @PathVariable("openbetId")
          List<Integer> openbetId) {
    List<HRMeeting> hrMeetings = service.getMeetingsByOpenbetIds(openbetId);
    return new ResponseEntity<List<HRMeeting>>(hrMeetings, HttpStatus.OK);
  }
}
