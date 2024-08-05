package com.ladbrokescoral.oxygen.cms.api.repository;

import com.ladbrokescoral.oxygen.cms.api.entity.BetPackEntity;
import java.time.Instant;
import java.util.List;
import org.springframework.stereotype.Repository;

@Repository
public interface BetPackEnablerRepository extends CustomMongoRepository<BetPackEntity> {
  List<BetPackEntity> findByBrandAndBetPackActiveTrue(String brand);

  List<BetPackEntity> findByBrandAndBetPackEndDateIsAfterOrMaxTokenExpirationDateIsAfter(
      String brand, Instant afterBetPackEndDate, Instant afterMaxTokenExpirationDate);
}
