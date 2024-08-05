package com.ladbrokescoral.oxygen.cms.api.repository;

import com.ladbrokescoral.oxygen.cms.api.entity.FanzoneNewGamingPopUp;
import java.util.Optional;
import org.springframework.data.mongodb.repository.Query;

public interface FanzonesNewGamingPopUpRepository
    extends CustomMongoRepository<FanzoneNewGamingPopUp> {

  @Query("{'brand': ?0}")
  Optional<FanzoneNewGamingPopUp> findAllByBrand(String brand);

  @Query("{'brand': ?0,'id': ?1}")
  Optional<FanzoneNewGamingPopUp> findAllByBrandAndId(String brand, String id);
}
