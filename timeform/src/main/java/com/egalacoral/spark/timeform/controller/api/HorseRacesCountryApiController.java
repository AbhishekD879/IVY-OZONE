package com.egalacoral.spark.timeform.controller.api;

import com.egalacoral.spark.timeform.model.horseracing.HRCountry;
import com.egalacoral.spark.timeform.service.horseracing.HorseRacingCountriesService;
import io.swagger.annotations.ApiParam;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.PathVariable;

@javax.annotation.Generated(
    value = "class io.swagger.codegen.languages.SpringCodegen",
    date = "2016-09-19T14:33:52.182Z")
@Controller
public class HorseRacesCountryApiController implements HorseRacesCountryApi {

  @Autowired private HorseRacingCountriesService service;

  public ResponseEntity<HRCountry> countryCountryIdGet(
      @ApiParam(value = "ID of the country", required = true) @PathVariable("countryCode")
          String countryId) {
    return ResponseEntityBuilder.build(service.getCountry(countryId));
  }
}
