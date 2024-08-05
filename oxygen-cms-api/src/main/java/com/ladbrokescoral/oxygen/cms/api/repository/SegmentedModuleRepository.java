package com.ladbrokescoral.oxygen.cms.api.repository;

import com.ladbrokescoral.oxygen.cms.api.entity.DeviceType;
import com.ladbrokescoral.oxygen.cms.api.entity.segment.SegmentedModule;
import java.util.List;

public interface SegmentedModuleRepository extends CustomMongoRepository<SegmentedModule> {
  List<SegmentedModule> findByModuleNameAndChannelAndBrand(
      String moduleName, DeviceType mobile, String brand);
}
