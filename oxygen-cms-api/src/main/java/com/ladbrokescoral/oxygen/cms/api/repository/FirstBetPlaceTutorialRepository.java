package com.ladbrokescoral.oxygen.cms.api.repository;

import com.ladbrokescoral.oxygen.cms.api.entity.onboarding.FirstBetPlaceTutorial;
import java.time.Instant;
import java.util.List;
import org.springframework.data.mongodb.repository.Query;

public interface FirstBetPlaceTutorialRepository
    extends IOnBoardingRepository<FirstBetPlaceTutorial> {

  @Query("{ brand : ?0,isEnable : ?1,'displayFrom':{'$lte':?2},'displayTo':{'$gte':?2} }")
  List<FirstBetPlaceTutorial> findByBrandAndIsEnabledAndNotExpired(
      String brand, boolean b, Instant now);
}
