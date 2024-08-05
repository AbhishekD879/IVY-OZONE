package com.egalacoral.spark.timeform.controller.api;

import com.egalacoral.spark.timeform.model.greyhound.Performance;
import com.egalacoral.spark.timeform.service.greyhound.TimeformPerformanceService;
import io.swagger.annotations.ApiParam;
import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestParam;

@javax.annotation.Generated(
    value = "class io.swagger.codegen.languages.SpringCodegen",
    date = "2016-09-02T07:48:35.998Z")
@Controller
public class GrayhoundRacesPerformancesApiController implements GrayhoundRacesPerformancesApi {

  @Autowired private TimeformPerformanceService service;

  @Override
  public ResponseEntity<List<Performance>> performancesGet(
      @ApiParam(value = "Returns only the first n the results")
          @RequestParam(value = "top", required = false)
          Integer top,
      @ApiParam(value = "Skips the first n results") @RequestParam(value = "skip", required = false)
          Integer skip,
      @ApiParam(value = "Sorts the results. Example : +greyhoundFullName,-performanceId")
          @RequestParam(value = "orderby", required = false)
          String orderby,
      @ApiParam(
              value =
                  "Filters the results, based on a Boolean condition. [Filters format](filters.html)")
          @RequestParam(value = "filter", required = false)
          String filter) {
    List<Performance> performances = service.getPerformances(filter, orderby, top, skip);
    return new ResponseEntity<List<Performance>>(performances, HttpStatus.OK);
  }
}
