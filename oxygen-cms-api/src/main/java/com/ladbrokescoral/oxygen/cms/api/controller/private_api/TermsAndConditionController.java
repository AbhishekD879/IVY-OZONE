package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.dto.TermsAndConditionDto;
import com.ladbrokescoral.oxygen.cms.api.entity.TermsAndCondition;
import com.ladbrokescoral.oxygen.cms.api.service.TermsAndConditionService;
import javax.validation.Valid;
import org.modelmapper.ModelMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class TermsAndConditionController extends AbstractSortableController<TermsAndCondition> {

  ModelMapper mapper;
  private TermsAndConditionService termsAndConditionService;

  @Autowired
  public TermsAndConditionController(
      TermsAndConditionService termsAndConditionService, ModelMapper mapper) {
    super(termsAndConditionService);
    this.termsAndConditionService = termsAndConditionService;
    this.mapper = mapper;
  }

  @GetMapping("termsandcondition/{brand}")
  public TermsAndCondition readOneByBrand(@PathVariable("brand") String brand) {
    TermsAndCondition termsAndCondition = termsAndConditionService.findOneByBrand(brand);

    return populateCreatorAndUpdater(termsAndCondition);
  }

  @PostMapping("termsandcondition")
  public ResponseEntity<TermsAndCondition> create(@Valid @RequestBody TermsAndConditionDto dto) {
    return super.create(mapper.map(dto, TermsAndCondition.class));
  }

  @PutMapping("termsandcondition/{id}")
  public TermsAndCondition update(
      @PathVariable String id, @Valid @RequestBody TermsAndConditionDto dto) {
    return super.update(id, mapper.map(dto, TermsAndCondition.class));
  }

  @DeleteMapping("termsandcondition/{brand}")
  public ResponseEntity<TermsAndCondition> deleteByBrand(@PathVariable("brand") String brand) {
    termsAndConditionService.deleteByBrand(brand);
    return ResponseEntity.ok().body(null);
  }
}
