package com.egalacoral.spark.timeform.controller.api;

import com.egalacoral.spark.timeform.model.horseracing.HRHorse;
import com.egalacoral.spark.timeform.service.horseracing.HorseRacingHorseService;
import io.swagger.annotations.ApiParam;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.PathVariable;

@javax.annotation.Generated(
    value = "class io.swagger.codegen.languages.SpringCodegen",
    date = "2016-09-19T14:33:52.182Z")
@Controller
public class HorseRacesHorseApiController implements HorseRacesHorseApi {

  @Autowired private HorseRacingHorseService service;

  public ResponseEntity<HRHorse> horseHorseIdGet(
      @ApiParam(value = "ID of the horse", required = true) @PathVariable("horseId")
          String horseId) {
    return ResponseEntityBuilder.build(service.getHorse(horseId));
  }
}
