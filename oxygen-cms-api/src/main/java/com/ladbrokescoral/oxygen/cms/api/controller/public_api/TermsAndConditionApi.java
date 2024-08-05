package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import com.ladbrokescoral.oxygen.cms.api.dto.TermsAndConditionDto;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.TermsAndConditionPublicService;
import java.util.Optional;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class TermsAndConditionApi implements Public {
  private final TermsAndConditionPublicService service;

  @Autowired
  public TermsAndConditionApi(TermsAndConditionPublicService service) {
    this.service = service;
  }

  @GetMapping(value = "{brand}/termsandcondition")
  public ResponseEntity<TermsAndConditionDto> findTermsAndConditionByBrand(
      @PathVariable String brand) {
    Optional<TermsAndConditionDto> optionalTermsAndCondition =
        service.findTermsAndConditionByBrand(brand);
    return optionalTermsAndCondition.isPresent()
        ? new ResponseEntity<>(optionalTermsAndCondition.get(), HttpStatus.OK)
        : new ResponseEntity<>(HttpStatus.NO_CONTENT);
  }
}
