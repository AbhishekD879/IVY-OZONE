package com.ladbrokescoral.oxygen.bigcompetition.service.impl.module;

import com.ladbrokescoral.oxygen.bigcompetition.dto.module.AemModuleDto;
import com.ladbrokescoral.oxygen.bigcompetition.mapper.module.AemModuleDtoMapper;
import com.ladbrokescoral.oxygen.bigcompetition.service.AemModuleService;
import com.ladbrokescoral.oxygen.cms.client.model.CompetitionModule;
import org.springframework.stereotype.Service;

@Service
// @Slf4j
public class AemModuleServiceImpl implements AemModuleService {

  @Override
  public AemModuleDto process(CompetitionModule module) {
    return AemModuleDtoMapper.INSTANCE.toDto(module);
  }
}
