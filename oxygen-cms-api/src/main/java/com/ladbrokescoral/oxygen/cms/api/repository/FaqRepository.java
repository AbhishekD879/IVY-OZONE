package com.ladbrokescoral.oxygen.cms.api.repository;

import com.ladbrokescoral.oxygen.cms.api.entity.Faq;
import java.util.List;

public interface FaqRepository extends CustomMongoRepository<Faq> {
  List<Faq> findAllByBrandOrderBySortOrderAsc(String brand);
}
