package com.ladbrokescoral.oxygen.cms.api.repository;

import com.ladbrokescoral.oxygen.cms.api.entity.StreamAndBet;
import java.util.Optional;

public interface StreamAndBetRepository extends CustomMongoRepository<StreamAndBet> {

  Optional<StreamAndBet> findOneByBrand(String brand);
}
