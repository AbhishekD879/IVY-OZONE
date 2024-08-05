package com.ladbrokescoral.oxygen.cms.api.repository;

import java.util.List;

public interface FindByRepository<T> {
  List<T> findAllByBrandAndDisabledOrderBySortOrderAsc(String brand, Boolean disabled);
}
