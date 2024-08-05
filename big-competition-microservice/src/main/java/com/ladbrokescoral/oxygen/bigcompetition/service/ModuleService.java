package com.ladbrokescoral.oxygen.bigcompetition.service;

import com.ladbrokescoral.oxygen.bigcompetition.dto.module.CompetitionModuleDto;
import com.ladbrokescoral.oxygen.cms.client.model.CompetitionModule;

@FunctionalInterface
public interface ModuleService {
  CompetitionModuleDto process(CompetitionModule source);
}
