package com.ladbrokescoral.oxygen.cms.api.repository;

import com.ladbrokescoral.oxygen.cms.api.entity.Fanzone;
import java.util.List;
import java.util.Optional;
import org.springframework.data.mongodb.repository.Query;

public interface FanzonesRepository extends CustomMongoRepository<Fanzone> {

  @Query("{'brand': ?0}")
  Optional<List<Fanzone>> findAllFanzonesByBrand(String brand);

  @Query("{'brand': ?0,'?1': ?2}")
  Optional<Fanzone> findByBrandAndColumn(String brand, String column, String val);
}
