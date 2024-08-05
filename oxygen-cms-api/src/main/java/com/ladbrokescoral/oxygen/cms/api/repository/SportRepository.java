package com.ladbrokescoral.oxygen.cms.api.repository;

import com.ladbrokescoral.oxygen.cms.api.entity.Sport;
import java.util.List;

public interface SportRepository extends CustomMongoRepository<Sport> {
  List<Sport> findAllByBrandOrderBySortOrderAsc(String brand);

  List<Sport> findAllByBrandAndDisabledOrderBySortOrderAsc(String brand, Boolean disabled);

  List<Sport> findByImageTitleContainingIgnoreCaseOrderBySortOrderAsc(String sportName);

  List<Sport> findByImageTitleContainingIgnoreCaseAndBrandIgnoreCaseOrderBySortOrderAsc(
      String sportName, String brand);
}
