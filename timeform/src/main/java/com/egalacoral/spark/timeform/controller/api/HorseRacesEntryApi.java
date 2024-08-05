package com.egalacoral.spark.timeform.controller.api;

import com.egalacoral.spark.timeform.model.horseracing.HREntry;
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
@Api(value = "entry", description = " ", tags = "Horses Entries")
public interface HorseRacesEntryApi extends HorseRacesApiBase {

  @ApiOperation(
      value = "",
      notes = "",
      response = HREntry.class,
      responseContainer = "List",
      tags = {})
  @ApiResponses(
      value = {
        @ApiResponse(
            code = 200,
            message = "Return the race with entry OpenBet ID",
            response = HREntry.class)
      })
  @RequestMapping(
      value = "/entry/{openbetId}",
      produces = {"application/json"},
      method = RequestMethod.GET)
  ResponseEntity<List<HREntry>> entryOpenbetIdGet(
      @ApiParam(value = "Comma separated list of OpenBet ID for race", required = true)
          @PathVariable("openbetId")
          List<Integer> openbetId);
}
