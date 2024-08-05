package com.ladbrokescoral.oxygen.cms.api.repository;

import com.ladbrokescoral.oxygen.cms.api.entity.StaticBlock;
import java.util.Optional;

public interface StaticBlockRepository extends CustomMongoRepository<StaticBlock> {

  Optional<StaticBlock> findFirstByBrandAndUriAndEnabled(String brand, String uri, Boolean enabled);
}
