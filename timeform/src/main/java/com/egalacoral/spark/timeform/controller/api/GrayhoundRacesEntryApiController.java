package com.egalacoral.spark.timeform.controller.api;

import com.egalacoral.spark.timeform.model.greyhound.Entry;
import com.egalacoral.spark.timeform.service.greyhound.TimeformEntriesService;
import io.swagger.annotations.ApiParam;
import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.PathVariable;

@javax.annotation.Generated(
    value = "class io.swagger.codegen.languages.SpringCodegen",
    date = "2016-09-02T07:48:35.998Z")
@Controller
public class GrayhoundRacesEntryApiController implements GrayhoundRacesEntryApi {

  @Autowired private TimeformEntriesService service;

  @Override
  public ResponseEntity<Entry> entryEntryIdGet(
      @ApiParam(value = "ID of the entry", required = true) @PathVariable("entryId")
          Integer entryId) {
    return ResponseEntityBuilder.build(service.getEntry(entryId));
  }

  @Override
  public ResponseEntity<List<Entry>> entryOpenbetIdOpenbetGet(
      @ApiParam(value = "Comma separated list of OpenBet ID of entry", required = true)
          @PathVariable("openbetId")
          List<Integer> openbetId) {
    return ResponseEntityBuilder.build(service.getEntryByOpenbetId(openbetId));
  }
}
