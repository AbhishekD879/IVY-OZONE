package com.egalacoral.spark.timeform.controller.api;

import com.egalacoral.spark.timeform.model.greyhound.Race;
import com.egalacoral.spark.timeform.service.greyhound.TimeformRacesService;
import io.swagger.annotations.ApiParam;
import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.PathVariable;

@javax.annotation.Generated(
    value = "class io.swagger.codegen.languages.SpringCodegen",
    date = "2016-09-02T07:48:35.998Z")
@Controller
public class GrayhoundRacesRaceApiController implements GrayhoundRacesRaceApi {

  @Autowired private TimeformRacesService service;

  @Override
  public ResponseEntity<List<Race>> raceOpenbetIdOpenbetGet(
      @ApiParam(value = "Comma separated list of OpenBet ID of the race", required = true)
          @PathVariable("openbetId")
          List<Integer> openbetId) {
    return ResponseEntityBuilder.build(service.getRaceByOpenbetId(openbetId));
  }

  @Override
  public ResponseEntity<Race> raceRaceIdGet(
      @ApiParam(value = "ID of the race", required = true) @PathVariable("raceId") Integer raceId) {
    return ResponseEntityBuilder.build(service.getRace(raceId));
  }
}
