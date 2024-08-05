package com.ladbrokescoral.oxygen.cms.api.repository;

import com.ladbrokescoral.oxygen.cms.api.entity.FiveASideFormation;
import java.util.List;

public interface FiveASideFormationRepository extends CustomMongoRepository<FiveASideFormation> {
  List<FiveASideFormation> findAllByBrandOrderBySortOrderAsc(String brand);
}
