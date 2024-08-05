package com.egalacoral.spark.timeform.controller.api;

import com.egalacoral.spark.timeform.model.horseracing.HRHorse;
import com.egalacoral.spark.timeform.service.horseracing.HorseRacingHorseService;
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
public class HorseRacesHorsesApiController implements HorseRacesHorsesApi {

  @Autowired private HorseRacingHorseService service;

  public ResponseEntity<List<HRHorse>> horsesGet(
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
    List<HRHorse> horses = service.getHorses(filter, orderby, top, skip);
    return new ResponseEntity<List<HRHorse>>(horses, HttpStatus.OK);
  }
}