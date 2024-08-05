package com.ladbrokescoral.oxygen.cms.api.repository;

import com.ladbrokescoral.oxygen.cms.api.entity.FanzoneNewSeason;
import java.util.Optional;
import org.springframework.data.mongodb.repository.Query;

public interface FanzonesNewSeasonRepository extends CustomMongoRepository<FanzoneNewSeason> {

  @Query("{'brand': ?0}")
  Optional<FanzoneNewSeason> findAllByBrand(String brand);

  @Query("{'brand': ?0,'id': ?1}")
  Optional<FanzoneNewSeason> findAllByBrandAndId(String brand, String id);
}
