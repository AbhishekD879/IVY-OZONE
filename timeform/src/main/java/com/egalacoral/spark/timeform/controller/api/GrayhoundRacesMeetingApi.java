package com.egalacoral.spark.timeform.controller.api;

import com.egalacoral.spark.timeform.model.greyhound.Meeting;
import io.swagger.annotations.Api;
import io.swagger.annotations.ApiOperation;
import io.swagger.annotations.ApiParam;
import io.swagger.annotations.ApiResponse;
import io.swagger.annotations.ApiResponses;
import java.util.List;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;

@javax.annotation.Generated(
    value = "class io.swagger.codegen.languages.SpringCodegen",
    date = "2016-09-02T07:48:35.998Z")
@Api(value = "meeting", description = " ", tags = "Greyhounds Meetings")
public interface GrayhoundRacesMeetingApi extends GrayhoundRacesApiBase {

  @ApiOperation(
      value = "",
      notes = "",
      response = Meeting.class,
      tags = {})
  @ApiResponses(
      value = {
        @ApiResponse(
            code = 200,
            message = "Sends the meeting with entry ID",
            response = Meeting.class)
      })
  @RequestMapping(
      value = "/meeting/{meetingId}",
      produces = {"application/json"},
      method = RequestMethod.GET)
  ResponseEntity<Meeting> meetingMeetingIdGet(
      @ApiParam(value = "ID of the meeting", required = true) @PathVariable("meetingId")
          Integer meetingId);

  @ApiOperation(
      value = "",
      notes = "",
      response = Meeting.class,
      tags = {})
  @ApiResponses(
      value = {
        @ApiResponse(
            code = 200,
            message = "Sends the meeting with entry OpenBet ID",
            response = Meeting.class)
      })
  @RequestMapping(
      value = "/meeting/{openbetId}/openbet",
      produces = {"application/json"},
      method = RequestMethod.GET)
  ResponseEntity<List<Meeting>> meetingOpenbetIdOpenbetGet(
      @ApiParam(value = "Comma separated list of OpenBet ID of the meeting", required = true)
          @PathVariable("openbetId")
          List<Integer> openbetId);
}
