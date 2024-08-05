package com.ladbrokescoral.oxygen.cms.api.repository;

import com.ladbrokescoral.oxygen.cms.api.entity.ArcProfile;
import java.util.List;
import java.util.Optional;

public interface ArcProfileRepository extends CustomMongoRepository<ArcProfile> {
  Optional<ArcProfile> findByBrandAndModelRiskLevelAndReasonCode(
      String brand, Integer modelAndRiskLevel, Integer reasonCode);

  Optional<List<ArcProfile>> findAllByBrand(String brand);

  Long deleteArcProfileByBrandAndModelRiskLevelAndReasonCode(
      String brand, Integer modelAndRiskLevel, Integer reasonCode);
}
