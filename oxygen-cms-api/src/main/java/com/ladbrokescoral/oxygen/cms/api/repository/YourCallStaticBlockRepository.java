package com.ladbrokescoral.oxygen.cms.api.repository;

import com.ladbrokescoral.oxygen.cms.api.entity.YourCallStaticBlock;
import java.util.List;

public interface YourCallStaticBlockRepository extends CustomMongoRepository<YourCallStaticBlock> {
  List<YourCallStaticBlock> findAllByBrandAndEnabled(String brand, Boolean enabled);

  List<YourCallStaticBlock> findAllByBrandAndEnabledAndFiveASide(
      String brand, Boolean enabled, Boolean fiveASide);
}
