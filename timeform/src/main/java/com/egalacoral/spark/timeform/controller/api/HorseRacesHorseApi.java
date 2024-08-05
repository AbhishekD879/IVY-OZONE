package com.egalacoral.spark.timeform.controller.api;

import com.egalacoral.spark.timeform.model.horseracing.HRHorse;
import io.swagger.annotations.Api;
import io.swagger.annotations.ApiOperation;
import io.swagger.annotations.ApiParam;
import io.swagger.annotations.ApiResponse;
import io.swagger.annotations.ApiResponses;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;

@javax.annotation.Generated(
    value = "class io.swagger.codegen.languages.SpringCodegen",
    date = "2016-09-19T14:33:52.182Z")
@Api(value = "horse", description = " ", tags = "Horses Horses")
public interface HorseRacesHorseApi extends HorseRacesApiBase {

  @ApiOperation(
      value = "",
      notes = "",
      response = HRHorse.class,
      tags = {})
  @ApiResponses(
      value = {
        @ApiResponse(
            code = 200,
            message = "Return the horse with entry ID",
            response = HRHorse.class)
      })
  @RequestMapping(
      value = "/horse/{horseId}",
      produces = {"application/json"},
      method = RequestMethod.GET)
  ResponseEntity<HRHorse> horseHorseIdGet(
      @ApiParam(value = "ID of the horse", required = true) @PathVariable("horseId")
          String horseId);
}
