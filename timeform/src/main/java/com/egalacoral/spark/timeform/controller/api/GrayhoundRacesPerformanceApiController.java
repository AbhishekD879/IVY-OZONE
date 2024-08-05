package com.egalacoral.spark.timeform.controller.api;

import com.egalacoral.spark.timeform.model.greyhound.Performance;
import com.egalacoral.spark.timeform.service.greyhound.TimeformPerformanceService;
import io.swagger.annotations.ApiParam;
import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.PathVariable;

@javax.annotation.Generated(
    value = "class io.swagger.codegen.languages.SpringCodegen",
    date = "2016-09-02T07:48:35.998Z")
@Controller
public class GrayhoundRacesPerformanceApiController implements GrayhoundRacesPerformanceApi {

  @Autowired private TimeformPerformanceService service;

  public ResponseEntity<List<Performance>> performanceGreyhoundIdGreyhoundGet(
      @ApiParam(value = "ID of the greyhound", required = true) @PathVariable("greyhoundId")
          Integer greyhoundId) {
    return new ResponseEntity<List<Performance>>(
        service.getPerformanceByGreyhoundId(greyhoundId), HttpStatus.OK);
  }

  public ResponseEntity<List<Performance>> performancePaMeetingIdMeetingGet(
      @ApiParam(value = "ID of the meeting", required = true) @PathVariable("paMeetingId")
          Integer paMeetingId) {
    return new ResponseEntity<List<Performance>>(
        service.getPerformanceByMeetingId(paMeetingId), HttpStatus.OK);
  }

  public ResponseEntity<Performance> performancePerformanceIdGet(
      @ApiParam(value = "ID of the performance", required = true) @PathVariable("performanceId")
          Integer performanceId) {
    return ResponseEntityBuilder.build(service.getPerformance(performanceId));
  }

  public ResponseEntity<List<Performance>> performanceRaceIdRaceGet(
      @ApiParam(value = "ID of the race", required = true) @PathVariable("raceId") Integer raceId) {
    return new ResponseEntity<List<Performance>>(
        service.getPerformanceByRaceId(raceId), HttpStatus.OK);
  }
}
