package com.ladbrokescoral.oxygen.cms.api.repository;

import com.ladbrokescoral.oxygen.cms.api.entity.RGYMetaInfoEntity;
import java.util.Optional;
import org.springframework.stereotype.Repository;

@Repository
public interface RGYMetaInfoRepository extends CustomMongoRepository<RGYMetaInfoEntity> {
  Optional<RGYMetaInfoEntity> findOneByBrand(String brand);
}
