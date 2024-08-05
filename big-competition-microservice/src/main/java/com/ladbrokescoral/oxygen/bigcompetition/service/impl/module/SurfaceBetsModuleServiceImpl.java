package com.ladbrokescoral.oxygen.bigcompetition.service.impl.module;

import com.ladbrokescoral.oxygen.bigcompetition.dto.module.SurfaceBetsModuleDto;
import com.ladbrokescoral.oxygen.bigcompetition.mapper.module.SurfaceBetsModuleMapper;
import com.ladbrokescoral.oxygen.bigcompetition.service.SurfaceBetsModuleService;
import com.ladbrokescoral.oxygen.cms.client.model.CompetitionModule;
import org.springframework.stereotype.Service;

@Service
public class SurfaceBetsModuleServiceImpl implements SurfaceBetsModuleService {
  @Override
  public SurfaceBetsModuleDto process(CompetitionModule module) {
    return SurfaceBetsModuleMapper.INSTANCE.toDto(module);
  }
}
