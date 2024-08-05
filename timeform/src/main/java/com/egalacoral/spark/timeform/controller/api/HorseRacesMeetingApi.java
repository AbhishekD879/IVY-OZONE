package com.egalacoral.spark.timeform.controller.api;

import com.egalacoral.spark.timeform.model.horseracing.HRMeeting;
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
    date = "2016-09-19T14:33:52.182Z")
@Api(value = "meeting", description = " ", tags = "Horses Meetings")
public interface HorseRacesMeetingApi extends HorseRacesApiBase {

  @ApiOperation(
      value = "",
      notes = "",
      response = HRMeeting.class,
      responseContainer = "List",
      tags = {})
  @ApiResponses(
      value = {
        @ApiResponse(
            code = 200,
            message = "Sends the meetings with entry OpenBet ID",
            response = HRMeeting.class)
      })
  @RequestMapping(
      value = "/meeting/{openbetId}",
      produces = {"application/json"},
      method = RequestMethod.GET)
  ResponseEntity<List<HRMeeting>> meetingOpenbetIdGet(
      @ApiParam(value = "Comma separated list of OpenBet ID of meeting", required = true)
          @PathVariable("openbetId")
          List<Integer> openbetId);
}
