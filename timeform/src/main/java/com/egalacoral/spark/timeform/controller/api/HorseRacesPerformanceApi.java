package com.egalacoral.spark.timeform.controller.api;

import com.egalacoral.spark.timeform.model.horseracing.HRPerformance;
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
@Api(value = "performance", description = " ", tags = "Horses Perfomances")
public interface HorseRacesPerformanceApi extends HorseRacesApiBase {

  @ApiOperation(
      value = "",
      notes = "",
      response = HRPerformance.class,
      tags = {})
  @ApiResponses(
      value = {
        @ApiResponse(
            code = 200,
            message = "Sends the performance with entry ID",
            response = HRPerformance.class)
      })
  @RequestMapping(
      value = "/performance/{performanceId}",
      produces = {"application/json"},
      method = RequestMethod.GET)
  ResponseEntity<HRPerformance> performancePerformanceIdGet(
      @ApiParam(value = "ID of the performance", required = true) @PathVariable("performanceId")
          String performanceId);
}
