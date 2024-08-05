package com.ladbrokescoral.oxygen.cms.api.repository;

import com.ladbrokescoral.oxygen.cms.api.entity.LuckyDipMapping;
import java.util.List;

public interface LuckyDipMappingRepository extends CustomMongoRepository<LuckyDipMapping> {

  List<LuckyDipMapping> findByBrandAndActiveTrue(String brand);

  List<LuckyDipMapping> findByBrandAndActiveTrueOrderBySortOrderAsc(String brand);
}
