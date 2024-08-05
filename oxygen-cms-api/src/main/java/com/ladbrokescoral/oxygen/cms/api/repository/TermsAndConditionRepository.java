package com.ladbrokescoral.oxygen.cms.api.repository;

import com.ladbrokescoral.oxygen.cms.api.entity.TermsAndCondition;
import java.util.List;
import java.util.Optional;

public interface TermsAndConditionRepository extends CustomMongoRepository<TermsAndCondition> {
  Optional<TermsAndCondition> findOneByBrand(String brand);

  List<TermsAndCondition> findAllByBrandOrderBySortOrderAsc(String brand);

  public void deleteByBrand(String brand);
}
