package com.egalacoral.spark.timeform.controller.api;

import com.egalacoral.spark.timeform.model.greyhound.Greyhound;
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
    date = "2016-09-02T07:48:35.998Z")
@Api(value = "greyhound", description = " ", tags = "Greyhounds Greyhounds")
@FunctionalInterface
public interface GrayhoundRacesGreyhoundApi extends GrayhoundRacesApiBase {

  @ApiOperation(
      value = "",
      notes = "",
      response = Greyhound.class,
      tags = {})
  @ApiResponses(
      value = {
        @ApiResponse(
            code = 200,
            message = "Sends the greyhound with entry ID",
            response = Greyhound.class)
      })
  @RequestMapping(
      value = "/greyhound/{greyhoundId}",
      produces = {"application/json"},
      method = RequestMethod.GET)
  ResponseEntity<Greyhound> greyhoundGreyhoundIdGet(
      @ApiParam(value = "ID of the greyhound", required = true) @PathVariable("greyhoundId")
          Integer greyhoundId);
}
