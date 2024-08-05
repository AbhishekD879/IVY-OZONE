package com.ladbrokescoral.oxygen.cms.api.repository;

import com.ladbrokescoral.oxygen.cms.api.entity.OddsBoostMessage;
import java.util.Optional;
import org.springframework.stereotype.Repository;

@Repository
public interface OddsBoostMessageRepository extends CustomMongoRepository<OddsBoostMessage> {
  Optional<OddsBoostMessage> findOneByBrand(String brand);
}
