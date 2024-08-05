package com.egalacoral.spark.timeform.controller.api;

import com.egalacoral.spark.timeform.model.greyhound.Greyhound;
import com.egalacoral.spark.timeform.service.greyhound.TimeformGreyhoundService;
import io.swagger.annotations.ApiParam;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.PathVariable;

@javax.annotation.Generated(
    value = "class io.swagger.codegen.languages.SpringCodegen",
    date = "2016-09-02T07:48:35.998Z")
@Controller
public class GrayhoundRacesGreyhoundApiController implements GrayhoundRacesGreyhoundApi {

  @Autowired private TimeformGreyhoundService service;

  @Override
  public ResponseEntity<Greyhound> greyhoundGreyhoundIdGet(
      @ApiParam(value = "ID of the greyhound", required = true) @PathVariable("greyhoundId")
          Integer greyhoundId) {
    return ResponseEntityBuilder.build(service.getGreyhound(greyhoundId));
  }
}
