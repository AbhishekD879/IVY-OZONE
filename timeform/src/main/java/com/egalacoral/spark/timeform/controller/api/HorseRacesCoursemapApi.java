package com.egalacoral.spark.timeform.controller.api;

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
@Api(value = "coursemap", description = " ", tags = "Horses CourseMap")
public interface HorseRacesCoursemapApi extends HorseRacesApiBase {

  @ApiOperation(
      value = "",
      notes = "",
      response = byte[].class,
      tags = {})
  @ApiResponses(
      value = {@ApiResponse(code = 200, message = "Course map image", response = byte[].class)})
  @RequestMapping(
      value = "/coursemap/{courseMapId}",
      produces = {"image/png"},
      method = RequestMethod.GET)
  ResponseEntity<byte[]> coursemapCourseMapIdGet(
      @ApiParam(value = "Course Map ID", required = true) @PathVariable("courseMapId")
          String courseMapId);
}
