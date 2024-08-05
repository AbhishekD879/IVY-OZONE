package com.egalacoral.spark.timeform.controller.api;

import com.egalacoral.spark.timeform.model.horseracing.HRCourse;
import com.egalacoral.spark.timeform.service.horseracing.HorseRacingCourseService;
import io.swagger.annotations.ApiParam;
import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestParam;

@javax.annotation.Generated(
    value = "class io.swagger.codegen.languages.SpringCodegen",
    date = "2016-09-19T14:33:52.182Z")
@Controller
public class HorseRacesCoursesApiController implements HorseRacesCoursesApi {

  @Autowired private HorseRacingCourseService service;

  public ResponseEntity<List<HRCourse>> coursesGet(
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
          String filter) {
    List<HRCourse> courses = service.getCourses(top, skip, orderby, filter);
    return new ResponseEntity<List<HRCourse>>(courses, HttpStatus.OK);
  }
}
