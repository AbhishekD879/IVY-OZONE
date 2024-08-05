package com.ladbrokescoral.oxygen.cms.api.repository;

import com.ladbrokescoral.oxygen.cms.api.entity.RGYConfigurationEntity;
import java.util.List;
import org.springframework.stereotype.Repository;

@Repository
public interface RGYConfigRepository extends CustomMongoRepository<RGYConfigurationEntity> {
  List<RGYConfigurationEntity> findByBrand(String brand);

  RGYConfigurationEntity findByBrandAndReasonCodeAndRiskLevelCodeAndBonusSuppressionTrue(
      String brand, int reasonCode, int riskLevelCode);

  RGYConfigurationEntity findByBrandAndReasonCodeAndRiskLevelCode(
      String brand, int reasonCode, int riskLevelCode);

  List<RGYConfigurationEntity> findByBrandAndBonusSuppressionTrue(String brand);
}
