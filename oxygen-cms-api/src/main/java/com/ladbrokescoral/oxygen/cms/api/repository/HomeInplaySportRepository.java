package com.ladbrokescoral.oxygen.cms.api.repository;

import com.ladbrokescoral.oxygen.cms.api.entity.HomeInplaySport;
import java.util.List;

public interface HomeInplaySportRepository extends CustomSegmentRepository<HomeInplaySport> {

  List<HomeInplaySport> findByCategoryIdAndBrand(String categoryId, String brand);
}
