package com.egalacoral.spark.timeform.controller.api;

import com.egalacoral.spark.timeform.model.greyhound.Entry;
import io.swagger.annotations.Api;
import io.swagger.annotations.ApiOperation;
import io.swagger.annotations.ApiParam;
import io.swagger.annotations.ApiResponse;
import io.swagger.annotations.ApiResponses;
import java.util.List;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;

@javax.annotation.Generated(
    value = "class io.swagger.codegen.languages.SpringCodegen",
    date = "2016-09-02T07:48:35.998Z")
@Api(value = "entry", description = " ", tags = "Greyhounds Entries")
public interface GrayhoundRacesEntryApi extends GrayhoundRacesApiBase {

  @ApiOperation(
      value = "",
      notes = "",
      response = Entry.class,
      tags = {})
  @ApiResponses(
      value = {
        @ApiResponse(code = 200, message = "Sends the entry with entry Id", response = Entry.class)
      })
  @RequestMapping(
      value = "/entry/{entryId}",
      produces = {"application/json"},
      method = RequestMethod.GET)
  ResponseEntity<Entry> entryEntryIdGet(
      @ApiParam(value = "ID of the entry", required = true) @PathVariable("entryId")
          Integer entryId);

  @ApiOperation(
      value = "",
      notes = "",
      response = Entry.class,
      tags = {})
  @ApiResponses(
      value = {
        @ApiResponse(
            code = 200,
            message = "Sends the entry with OpenBet Id",
            response = Entry.class)
      })
  @RequestMapping(
      value = "/entry/{openbetId}/openbet",
      produces = {"application/json"},
      method = RequestMethod.GET)
  ResponseEntity<List<Entry>> entryOpenbetIdOpenbetGet(
      @ApiParam(value = "Comma separated list of OpenBet ID of the entry", required = true)
          @PathVariable("openbetId")
          List<Integer> openbetId);
}
