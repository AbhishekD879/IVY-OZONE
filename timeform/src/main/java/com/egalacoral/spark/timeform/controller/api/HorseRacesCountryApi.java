package com.egalacoral.spark.timeform.controller.api;

import com.egalacoral.spark.timeform.model.horseracing.HRCountry;
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
@Api(value = "country", description = " ", tags = "Horses Countries")
public interface HorseRacesCountryApi extends HorseRacesApiBase {

  @ApiOperation(
      value = "",
      notes = "",
      response = HRCountry.class,
      tags = {})
  @ApiResponses(
      value = {
        @ApiResponse(
            code = 200,
            message = "Return the country with entry ID",
            response = HRCountry.class)
      })
  @RequestMapping(
      value = "/country/{countryCode}",
      produces = {"application/json"},
      method = RequestMethod.GET)
  ResponseEntity<HRCountry> countryCountryIdGet(
      @ApiParam(value = "ID of the country", required = true) @PathVariable("countryCode")
          String countryId);
}
