package com.ladbrokescoral.oxygen.cms.api.repository;

import com.ladbrokescoral.oxygen.cms.api.entity.LuckyDipV2Config;
import java.util.List;
import java.util.Optional;

public interface LuckyDipV2ConfigRepository extends CustomMongoRepository<LuckyDipV2Config> {
  Optional<LuckyDipV2Config> findByBrandAndLuckyDipConfigLevelId(
      String brand, String configLevelId);

  List<LuckyDipV2Config> findAllByBrandAndStatusTrue(String brand);
}
