package com.ladbrokescoral.oxygen.cms.api.repository;

import com.ladbrokescoral.oxygen.cms.api.entity.CompetitionModule;
import com.ladbrokescoral.oxygen.cms.api.entity.CompetitionModuleType;
import java.util.List;

public interface CompetitionModuleRepository extends CustomMongoRepository<CompetitionModule> {

  List<CompetitionModule> findByType(CompetitionModuleType competitionModuleType);
}
