package com.ladbrokescoral.oxygen.cms.api.service.public_api;

import com.ladbrokescoral.oxygen.cms.api.dto.TermsAndConditionDto;
import com.ladbrokescoral.oxygen.cms.api.entity.TermsAndCondition;
import com.ladbrokescoral.oxygen.cms.api.exception.NotFoundException;
import com.ladbrokescoral.oxygen.cms.api.service.TermsAndConditionService;
import java.util.List;
import java.util.Optional;
import org.modelmapper.ModelMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class TermsAndConditionPublicService {
  private final TermsAndConditionService service;

  private ModelMapper modelMapper;

  @Autowired
  public TermsAndConditionPublicService(TermsAndConditionService service, ModelMapper modelMapper) {
    this.service = service;
    this.modelMapper = modelMapper;
  }

  public List<TermsAndCondition> findByBrand(String brand) {
    return service.findAllByBrandSorted(brand);
  }

  public Optional<TermsAndCondition> findOneByBrand(String brand) {
    return service.findOptionalByBrand(brand);
  }

  public Optional<TermsAndConditionDto> findTermsAndConditionByBrand(String brand) {
    Optional<TermsAndCondition> optionalTermsAndCondition = service.findOptionalByBrand(brand);
    if (optionalTermsAndCondition.isPresent()) {
      return Optional.of(
          modelMapper.map(optionalTermsAndCondition.get(), TermsAndConditionDto.class));
    } else {
      throw new NotFoundException();
    }
  }
}
