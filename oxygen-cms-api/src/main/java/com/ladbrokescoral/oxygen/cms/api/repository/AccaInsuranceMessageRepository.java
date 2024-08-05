package com.ladbrokescoral.oxygen.cms.api.repository;

import com.ladbrokescoral.oxygen.cms.api.entity.AccaInsuranceMessage;
import java.util.Optional;
import org.springframework.stereotype.Repository;

@Repository
public interface AccaInsuranceMessageRepository
    extends CustomMongoRepository<AccaInsuranceMessage> {
  Optional<AccaInsuranceMessage> findOneByBrand(String brand);
}
