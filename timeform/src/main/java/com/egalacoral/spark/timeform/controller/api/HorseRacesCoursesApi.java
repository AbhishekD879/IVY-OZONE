package com.egalacoral.spark.timeform.controller.api;

import com.egalacoral.spark.timeform.model.horseracing.HRCourse;
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
@Api(value = "courses", description = " ", tags = "Horses Courses")
public interface HorseRacesCoursesApi extends HorseRacesApiBase {

  @ApiOperation(
      value = "",
      notes = "",
      response = HRCourse.class,
      responseContainer = "List",
      tags = {})
  @ApiResponses(
      value = {@ApiResponse(code = 200, message = "List all courses", response = HRCourse.class)})
  @RequestMapping(
      value = "/courses",
      produces = {"application/json"},
      method = RequestMethod.GET)
  ResponseEntity<List<HRCourse>> coursesGet(
      @ApiParam(value = "Returns only the first n the results")
          @RequestParam(value = "top", required = false)
          Integer top,
      @ApiParam(value = "Skips the first n results") @RequestParam(value = "skip", required = false)
          Integer skip,
      @ApiParam(value = "Sorts the results") @RequestParam(value = "orderby", required = false)
          String orderby,
      @ApiParam(value = "Filters the results, based on a Boolean condition.")
          @RequestParam(value = "filter", required = false)
          String filter);
}