package com.ladbrokescoral.oxygen.cms.api.repository;

import com.ladbrokescoral.oxygen.cms.api.entity.QualificationRule;
import java.util.Optional;

public interface QualificationRuleRepository extends CustomMongoRepository<QualificationRule> {

  Optional<QualificationRule> findOneByBrand(String brand);

  Optional<QualificationRule> findOneByBrandAndEnabledIsTrue(String brand);

  boolean existsByBrand(String brand);
}
