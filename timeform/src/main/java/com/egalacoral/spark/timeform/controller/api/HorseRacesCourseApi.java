package com.egalacoral.spark.timeform.controller.api;

import com.egalacoral.spark.timeform.model.horseracing.HRCourse;
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
@Api(value = "course", description = " ", tags = "Horses Courses")
public interface HorseRacesCourseApi extends HorseRacesApiBase {

  @ApiOperation(
      value = "",
      notes = "",
      response = HRCourse.class,
      tags = {})
  @ApiResponses(
      value = {
        @ApiResponse(
            code = 200,
            message = "Sends the course with entry ID",
            response = HRCourse.class)
      })
  @RequestMapping(
      value = "/course/{courseId}",
      produces = {"application/json"},
      method = RequestMethod.GET)
  ResponseEntity<HRCourse> courseCourseIdGet(
      @ApiParam(value = "ID of the courses", required = true) @PathVariable("courseId")
          Integer courseId);
}
