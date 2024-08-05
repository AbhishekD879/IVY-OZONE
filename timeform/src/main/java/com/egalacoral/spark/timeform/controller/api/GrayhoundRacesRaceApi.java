package com.egalacoral.spark.timeform.controller.api;

import com.egalacoral.spark.timeform.model.greyhound.Race;
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
@Api(value = "race", description = " ", tags = "Greyhounds Races")
public interface GrayhoundRacesRaceApi extends GrayhoundRacesApiBase {

  @ApiOperation(
      value = "",
      notes = "",
      response = Race.class,
      tags = {})
  @ApiResponses(
      value = {
        @ApiResponse(
            code = 200,
            message = "Sends the race with entry OpenBet ID",
            response = Race.class)
      })
  @RequestMapping(
      value = "/race/{openbetId}/openbet",
      produces = {"application/json"},
      method = RequestMethod.GET)
  ResponseEntity<List<Race>> raceOpenbetIdOpenbetGet(
      @ApiParam(value = "Comma separated list of OpenBet ID of the race", required = true)
          @PathVariable("openbetId")
          List<Integer> openbetId);

  @ApiOperation(
      value = "",
      notes = "",
      response = Race.class,
      tags = {})
  @ApiResponses(
      value = {
        @ApiResponse(code = 200, message = "Sends the race with entry ID", response = Race.class)
      })
  @RequestMapping(
      value = "/race/{raceId}",
      produces = {"application/json"},
      method = RequestMethod.GET)
  ResponseEntity<Race> raceRaceIdGet(
      @ApiParam(value = "ID of the race", required = true) @PathVariable("raceId") Integer raceId);
}
