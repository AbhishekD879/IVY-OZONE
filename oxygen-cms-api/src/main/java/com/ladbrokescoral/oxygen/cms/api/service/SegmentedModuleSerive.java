package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.entity.DeviceType;
import com.ladbrokescoral.oxygen.cms.api.entity.segment.SegmentedModule;
import com.ladbrokescoral.oxygen.cms.api.repository.SegmentedModuleRepository;
import java.util.List;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.util.CollectionUtils;

@Slf4j
@Service
public class SegmentedModuleSerive extends AbstractService<SegmentedModule> {

  private final SegmentedModuleRepository segmentedModuleRepository;

  public SegmentedModuleSerive(SegmentedModuleRepository segmentedModuleRepository) {
    super(segmentedModuleRepository);
    this.segmentedModuleRepository = segmentedModuleRepository;
  }

  public boolean isSegmentedModule(String moduleName, DeviceType deviceType, String brand) {
    List<SegmentedModule> segmentModule =
        segmentedModuleRepository.findByModuleNameAndChannelAndBrand(moduleName, deviceType, brand);
    return !CollectionUtils.isEmpty(segmentModule);
  }
}
