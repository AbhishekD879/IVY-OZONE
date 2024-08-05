package com.ladbrokescoral.oxygen.cms.api.repository;

import com.ladbrokescoral.oxygen.cms.api.entity.FanzoneClub;
import java.util.List;
import java.util.Optional;
import org.springframework.data.mongodb.repository.Query;

public interface FanzonesClubRepository extends CustomMongoRepository<FanzoneClub> {

  @Query("{'brand': ?0}")
  Optional<List<FanzoneClub>> findAllFanzonesByBrand(String brand);

  @Query("{'brand': ?0,'?1': ?2}")
  Optional<FanzoneClub> findByBrandAndColumn(String brand, String column, String val);
}
