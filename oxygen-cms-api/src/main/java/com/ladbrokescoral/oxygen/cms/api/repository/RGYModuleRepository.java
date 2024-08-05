package com.ladbrokescoral.oxygen.cms.api.repository;

import com.ladbrokescoral.oxygen.cms.api.entity.RGYModuleEntity;
import java.util.List;
import java.util.Optional;
import org.springframework.stereotype.Repository;

@Repository
public interface RGYModuleRepository extends CustomMongoRepository<RGYModuleEntity> {
  List<RGYModuleEntity> findByBrand(String brand);

  Optional<RGYModuleEntity> findById(String id);

  Optional<RGYModuleEntity> findByIdAndSubModuleEnabledTrue(String id);

  void deleteById(String rgyModuleId);
}
