package com.egalacoral.spark.timeform.controller.api;

import com.egalacoral.spark.timeform.model.horseracing.HRMeeting;
import io.swagger.annotations.Api;
import io.swagger.annotations.ApiOperation;
import io.swagger.annotations.ApiParam;
import io.swagger.annotations.ApiResponse;
import io.swagger.annotations.ApiResponses;
import java.util.List;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RequestParam;

@javax.annotation.Generated(
    value = "class io.swagger.codegen.languages.SpringCodegen",
    date = "2016-09-19T14:33:52.182Z")
@Api(value = "meetings", description = " ", tags = "Horses Meetings")
public interface HorseRacesMeetingsApi extends HorseRacesApiBase {

  @ApiOperation(
      value = "",
      notes = "",
      response = HRMeeting.class,
      responseContainer = "List",
      tags = {})
  @ApiResponses(
      value = {@ApiResponse(code = 200, message = "List all meetings", response = HRMeeting.class)})
  @RequestMapping(
      value = "/meetings",
      produces = {"application/json"},
      method = RequestMethod.GET)
  ResponseEntity<List<HRMeeting>> meetingsGet(
      @ApiParam(value = "Returns only the first n the results")
          @RequestParam(value = "top", required = false)
          Integer top,
      @ApiParam(value = "Skips the first n results") @RequestParam(value = "skip", required = false)
          Integer skip,
      @ApiParam(value = "Sorts the results") @RequestParam(value = "orderby", required = false)
          String orderby,
      @ApiParam(
              value =
                  "Filters the results, based on a Boolean condition. [Filters format](filters.html)")
          @RequestParam(value = "filter", required = false)
          String filter);
}
