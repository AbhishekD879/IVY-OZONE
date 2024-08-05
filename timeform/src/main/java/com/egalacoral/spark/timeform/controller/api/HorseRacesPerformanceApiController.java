package com.egalacoral.spark.timeform.controller.api;

import com.egalacoral.spark.timeform.model.horseracing.HRPerformance;
import com.egalacoral.spark.timeform.service.horseracing.HorseRacingPerformanceService;
import io.swagger.annotations.ApiParam;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.PathVariable;

@javax.annotation.Generated(
    value = "class io.swagger.codegen.languages.SpringCodegen",
    date = "2016-09-19T14:33:52.182Z")
@Controller
public class HorseRacesPerformanceApiController implements HorseRacesPerformanceApi {

  @Autowired private HorseRacingPerformanceService service;

  public ResponseEntity<HRPerformance> performancePerformanceIdGet(
      @ApiParam(value = "ID of the performance", required = true) @PathVariable("performanceId")
          String performanceId) {
    return ResponseEntityBuilder.build(service.getPerfomance(performanceId));
  }
}
