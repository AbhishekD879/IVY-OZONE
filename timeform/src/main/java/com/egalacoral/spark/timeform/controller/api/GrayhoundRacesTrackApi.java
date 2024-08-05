package com.egalacoral.spark.timeform.controller.api;

import com.egalacoral.spark.timeform.model.greyhound.Track;
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
@Api(value = "track", description = " ", tags = "Greyhounds Tracks")
@FunctionalInterface
public interface GrayhoundRacesTrackApi extends GrayhoundRacesApiBase {

  @ApiOperation(
      value = "",
      notes = "",
      response = Track.class,
      tags = {})
  @ApiResponses(
      value = {
        @ApiResponse(code = 200, message = "Sends the track with entry Id", response = Track.class)
      })
  @RequestMapping(
      value = "/track/{trackId}",
      produces = {"application/json"},
      method = RequestMethod.GET)
  ResponseEntity<Track> trackTrackIdGet(
      @ApiParam(value = "ID of the track", required = true) @PathVariable("trackId")
          Integer trackId);
}
