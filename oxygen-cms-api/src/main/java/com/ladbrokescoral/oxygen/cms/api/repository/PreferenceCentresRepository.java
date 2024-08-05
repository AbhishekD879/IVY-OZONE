package com.ladbrokescoral.oxygen.cms.api.repository;

import com.ladbrokescoral.oxygen.cms.api.entity.PreferenceCentre;
import java.util.Optional;
import org.springframework.data.mongodb.repository.Query;

public interface PreferenceCentresRepository extends CustomMongoRepository<PreferenceCentre> {

  // ps
  @Query("{'brand': ?0}")
  Optional<PreferenceCentre> findAllPreferencesByBrand(String brand);

  // ps
  @Query("{'brand': ?0,'?1': ?2}")
  Optional<PreferenceCentre> findByBrandAndColumn(String brand, String column, String val);

  @Query("{'brand': ?0,'pageName': ?1}")
  Optional<PreferenceCentre> findByBrandPageName(String brand, String pageName);
}
