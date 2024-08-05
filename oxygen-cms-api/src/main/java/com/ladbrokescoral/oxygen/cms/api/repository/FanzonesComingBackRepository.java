package com.ladbrokescoral.oxygen.cms.api.repository;

import com.ladbrokescoral.oxygen.cms.api.entity.FanzoneComingBack;
import java.util.Optional;
import org.springframework.data.mongodb.repository.Query;

public interface FanzonesComingBackRepository extends CustomMongoRepository<FanzoneComingBack> {

  @Query("{'brand': ?0}")
  Optional<FanzoneComingBack> findAllByBrand(String brand);

  @Query("{'brand': ?0,'id': ?1}")
  Optional<FanzoneComingBack> findAllByBrandAndId(String brand, String id);
}
