package com.egalacoral.spark.timeform.controller.api;

import com.egalacoral.spark.timeform.model.greyhound.Track;
import com.egalacoral.spark.timeform.service.greyhound.TimeformTrackService;
import io.swagger.annotations.ApiParam;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.PathVariable;

@javax.annotation.Generated(
    value = "class io.swagger.codegen.languages.SpringCodegen",
    date = "2016-09-02T07:48:35.998Z")
@Controller
public class GrayhoundRacesTrackApiController implements GrayhoundRacesTrackApi {

  @Autowired private TimeformTrackService service;

  @Override
  public ResponseEntity<Track> trackTrackIdGet(
      @ApiParam(value = "ID of the track", required = true) @PathVariable("trackId")
          Integer trackId) {
    return ResponseEntityBuilder.build(service.getTrack(trackId));
  }
}
