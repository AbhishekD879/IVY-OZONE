package com.ladbrokescoral.oxygen.cms.api.repository;

import com.ladbrokescoral.oxygen.cms.api.entity.freeride.FreeRideSplashPage;
import java.util.List;

public interface FreeRideSplashPageRepository extends CustomMongoRepository<FreeRideSplashPage> {
  List<FreeRideSplashPage> findAllByBrand(String brand);
}
