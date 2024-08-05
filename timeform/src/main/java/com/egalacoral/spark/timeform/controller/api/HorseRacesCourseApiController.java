package com.egalacoral.spark.timeform.controller.api;

import com.egalacoral.spark.timeform.model.horseracing.HRCourse;
import com.egalacoral.spark.timeform.service.horseracing.HorseRacingCourseService;
import io.swagger.annotations.ApiParam;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.PathVariable;

@javax.annotation.Generated(
    value = "class io.swagger.codegen.languages.SpringCodegen",
    date = "2016-09-19T14:33:52.182Z")
@Controller
public class HorseRacesCourseApiController implements HorseRacesCourseApi {

  @Autowired private HorseRacingCourseService service;

  public ResponseEntity<HRCourse> courseCourseIdGet(
      @ApiParam(value = "ID of the courses", required = true) @PathVariable("courseId")
          Integer courseId) {
    return ResponseEntityBuilder.build(service.getCourse(courseId));
  }
}
