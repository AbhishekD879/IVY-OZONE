package com.egalacoral.spark.timeform.controller.api;

import com.egalacoral.spark.timeform.model.greyhound.Performance;
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
@Api(value = "performance", description = " ", tags = "Greyhounds Performances")
public interface GrayhoundRacesPerformanceApi extends GrayhoundRacesApiBase {

  @ApiOperation(
      value = "",
      notes = "",
      response = Performance.class,
      tags = {})
  @ApiResponses(
      value = {
        @ApiResponse(
            code = 200,
            message = "Sends the performance for greyhound with entry ID",
            response = Performance.class)
      })
  @RequestMapping(
      value = "/performance/{greyhoundId}/greyhound",
      produces = {"application/json"},
      method = RequestMethod.GET)
  ResponseEntity<List<Performance>> performanceGreyhoundIdGreyhoundGet(
      @ApiParam(value = "ID of the greyhound", required = true) @PathVariable("greyhoundId")
          Integer greyhoundId);

  @ApiOperation(
      value = "",
      notes = "",
      response = Performance.class,
      tags = {})
  @ApiResponses(
      value = {
        @ApiResponse(
            code = 200,
            message = "Sends the performance for meeting with entry ID",
            response = Performance.class)
      })
  @RequestMapping(
      value = "/performance/{paMeetingId}/meeting",
      produces = {"application/json"},
      method = RequestMethod.GET)
  ResponseEntity<List<Performance>> performancePaMeetingIdMeetingGet(
      @ApiParam(value = "ID of the meeting", required = true) @PathVariable("paMeetingId")
          Integer paMeetingId);

  @ApiOperation(
      value = "",
      notes = "",
      response = Performance.class,
      tags = {})
  @ApiResponses(
      value = {
        @ApiResponse(
            code = 200,
            message = "Sends the performance with entry ID",
            response = Performance.class)
      })
  @RequestMapping(
      value = "/performance/{performanceId}",
      produces = {"application/json"},
      method = RequestMethod.GET)
  ResponseEntity<Performance> performancePerformanceIdGet(
      @ApiParam(value = "ID of the performance", required = true) @PathVariable("performanceId")
          Integer performanceId);

  @ApiOperation(
      value = "",
      notes = "",
      response = Performance.class,
      tags = {})
  @ApiResponses(
      value = {
        @ApiResponse(
            code = 200,
            message = "Sends the performance for race with entry ID",
            response = Performance.class)
      })
  @RequestMapping(
      value = "/performance/{raceId}/race",
      produces = {"application/json"},
      method = RequestMethod.GET)
  ResponseEntity<List<Performance>> performanceRaceIdRaceGet(
      @ApiParam(value = "ID of the race", required = true) @PathVariable("raceId") Integer raceId);
}
