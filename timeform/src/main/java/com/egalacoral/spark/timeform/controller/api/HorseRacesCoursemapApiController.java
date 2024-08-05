package com.egalacoral.spark.timeform.controller.api;

import com.egalacoral.spark.timeform.model.horseracing.HRCourseMapInfo;
import com.egalacoral.spark.timeform.service.horseracing.HorseRacingCourseMapService;
import io.swagger.annotations.ApiParam;
import java.util.Optional;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.PathVariable;

@javax.annotation.Generated(
    value = "class io.swagger.codegen.languages.SpringCodegen",
    date = "2016-09-19T14:33:52.182Z")
@Controller
public class HorseRacesCoursemapApiController implements HorseRacesCoursemapApi {

  @Autowired private HorseRacingCourseMapService horseRacingBatchService;

  public ResponseEntity<byte[]> coursemapCourseMapIdGet(
      @ApiParam(value = "Course Map ID", required = true) @PathVariable("courseMapId")
          String courseMapId) {
    byte[] bs = null;
    Optional<HRCourseMapInfo> info = horseRacingBatchService.getCourseMap(courseMapId);
    if (info.isPresent()) {
      bs = info.get().getCourseMap().getBytes();
    }
    return ResponseEntityBuilder.build(Optional.ofNullable(bs));
  }
}
