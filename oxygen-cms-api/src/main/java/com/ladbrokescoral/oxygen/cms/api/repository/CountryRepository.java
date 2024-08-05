package com.ladbrokescoral.oxygen.cms.api.repository;

import com.ladbrokescoral.oxygen.cms.api.entity.Country;
import java.util.List;

public interface CountryRepository extends CustomMongoRepository<Country> {
  List<Country> findAllByBrand(String brand);
}
