package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.entity.TermsAndCondition;
import com.ladbrokescoral.oxygen.cms.api.exception.BadRequestException;
import com.ladbrokescoral.oxygen.cms.api.exception.NotFoundException;
import com.ladbrokescoral.oxygen.cms.api.repository.TermsAndConditionRepository;
import java.util.List;
import java.util.Optional;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class TermsAndConditionService extends SortableService<TermsAndCondition> {
  private final TermsAndConditionRepository termsAndConditionRepository;

  @Autowired
  public TermsAndConditionService(TermsAndConditionRepository termsAndConditionRepository) {
    super(termsAndConditionRepository);
    this.termsAndConditionRepository = termsAndConditionRepository;
  }

  public List<TermsAndCondition> findAllByBrandSorted(String brand) {
    return termsAndConditionRepository.findAllByBrandOrderBySortOrderAsc(brand);
  }

  public TermsAndCondition findOneByBrand(String brand) {
    return termsAndConditionRepository.findOneByBrand(brand).orElseThrow(NotFoundException::new);
  }

  public Optional<TermsAndCondition> findOptionalByBrand(String brand) {
    return termsAndConditionRepository.findOneByBrand(brand);
  }

  @Override
  public TermsAndCondition prepareModelBeforeSave(TermsAndCondition termsAndCondition) {
    Optional<TermsAndCondition> mayBeEntity =
        termsAndConditionRepository.findOneByBrand(termsAndCondition.getBrand());
    if (mayBeEntity.isPresent() && termsAndCondition.isNew()) {
      throw new BadRequestException("there is already one entity present");
    }
    return termsAndCondition;
  }

  public void deleteByBrand(String brand) {
    termsAndConditionRepository.deleteByBrand(brand);
  }
}
