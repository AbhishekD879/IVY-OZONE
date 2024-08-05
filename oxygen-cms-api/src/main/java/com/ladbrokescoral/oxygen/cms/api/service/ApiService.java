package com.ladbrokescoral.oxygen.cms.api.service;

import java.util.List;

public interface ApiService<T> {

  List<T> findByBrand(String brand);
}
