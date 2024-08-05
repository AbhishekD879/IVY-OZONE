package com.ladbrokescoral.oxygen.cms.api.repository;

import com.ladbrokescoral.oxygen.cms.api.entity.FanzoneNewSignposting;
import java.util.Optional;
import org.springframework.data.mongodb.repository.Query;

public interface FanzonesNewSignpostingRepository
    extends CustomMongoRepository<FanzoneNewSignposting> {

  @Query("{'brand': ?0}")
  Optional<FanzoneNewSignposting> findAllByBrand(String brand);

  @Query("{'brand': ?0,'id': ?1}")
  Optional<FanzoneNewSignposting> findAllByBrandAndId(String brand, String id);
}
