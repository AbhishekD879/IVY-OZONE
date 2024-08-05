package com.egalacoral.spark.timeform.controller.api;

import com.egalacoral.spark.timeform.model.greyhound.Meeting;
import com.egalacoral.spark.timeform.service.greyhound.TimeformMeetingService;
import com.egalacoral.spark.timeform.timer.Timer;
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
public class GrayhoundRacesMeetingsApiController implements GrayhoundRacesMeetingsApi {

  @Autowired TimeformMeetingService service;

  @Override
  @Timer
  public ResponseEntity<List<Meeting>> meetingsGet(
      @ApiParam(value = "Returns only the first n the results")
          @RequestParam(value = "top", required = false)
          Integer top,
      @ApiParam(value = "Skips the first n results") @RequestParam(value = "skip", required = false)
          Integer skip,
      @ApiParam(value = "Sorts the results. Example : +trackShortName")
          @RequestParam(value = "orderby", required = false)
          String orderby,
      @ApiParam(
              value =
                  "Filters the results, based on a Boolean condition. [Filters format](filters.html) ")
          @RequestParam(value = "filter", required = false)
          String filter) {
    List<Meeting> meetings = service.getMeetings(filter, orderby, top, skip);
    return new ResponseEntity<List<Meeting>>(meetings, HttpStatus.OK);
  }
}
