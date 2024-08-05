package com.egalacoral.spark.timeform.controller.api;

import com.egalacoral.spark.timeform.model.horseracing.HREntry;
import com.egalacoral.spark.timeform.service.horseracing.HorseRacingStorageService;
import io.swagger.annotations.ApiParam;
import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.PathVariable;

@javax.annotation.Generated(
    value = "class io.swagger.codegen.languages.SpringCodegen",
    date = "2016-09-19T14:33:52.182Z")
@Controller
public class HorseRacesEntryApiController implements HorseRacesEntryApi {

  @Autowired private HorseRacingStorageService service;

  public ResponseEntity<List<HREntry>> entryOpenbetIdGet(
      @ApiParam(value = "Comma separated list of OpenBet ID for entry", required = true)
          @PathVariable("openbetId")
          List<Integer> openbetId) {
    List<HREntry> entries = service.getEntriesByOpenbetId(openbetId);
    return new ResponseEntity<List<HREntry>>(entries, HttpStatus.OK);
  }
}
