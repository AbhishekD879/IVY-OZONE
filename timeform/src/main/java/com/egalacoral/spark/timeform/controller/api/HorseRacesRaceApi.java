package com.egalacoral.spark.timeform.controller.api;

import com.egalacoral.spark.timeform.model.horseracing.HRRace;
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
@Api(value = "race", description = " ", tags = "Horses Races")
public interface HorseRacesRaceApi extends HorseRacesApiBase {

  @ApiOperation(
      value = "",
      notes = "",
      response = HRRace.class,
      responseContainer = "List",
      tags = {})
  @ApiResponses(
      value = {
        @ApiResponse(
            code = 200,
            message = "Sends the races with entry OpenBet ID",
            response = HRRace.class)
      })
  @RequestMapping(
      value = "/race/{openbetId}",
      produces = {"application/json"},
      method = RequestMethod.GET)
  ResponseEntity<List<HRRace>> raceOpenbetIdGet(
      @ApiParam(value = "Comma separated list of OpenBet IDs for entry", required = true)
          @PathVariable("openbetId")
          List<Integer> openbetId);
}
