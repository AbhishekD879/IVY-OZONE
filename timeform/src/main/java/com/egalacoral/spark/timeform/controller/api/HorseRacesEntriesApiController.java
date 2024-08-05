package com.egalacoral.spark.timeform.controller.api;

import com.egalacoral.spark.timeform.model.horseracing.HREntry;
import com.egalacoral.spark.timeform.service.horseracing.HorseRacingStorageService;
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
public class HorseRacesEntriesApiController implements HorseRacesEntriesApi {

  @Autowired private HorseRacingStorageService service;

  public ResponseEntity<List<HREntry>> entriesGet(
      @ApiParam(value = "Returns only the first n the results")
          @RequestParam(value = "top", required = false)
          Integer top,
      @ApiParam(value = "Skips the first n results") @RequestParam(value = "skip", required = false)
          Integer skip,
      @ApiParam(value = "Sorts the results") @RequestParam(value = "orderby", required = false)
          String orderby,
      @ApiParam(value = "Filters the results, based on a Boolean condition")
          @RequestParam(value = "filter", required = false)
          String filter) {
    List<HREntry> entries = service.getEntries(top, skip, orderby, filter);
    return new ResponseEntity<List<HREntry>>(entries, HttpStatus.OK);
  }
}
