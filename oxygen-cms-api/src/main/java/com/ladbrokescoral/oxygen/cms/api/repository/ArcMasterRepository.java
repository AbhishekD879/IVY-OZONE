package com.ladbrokescoral.oxygen.cms.api.repository;

import com.ladbrokescoral.oxygen.cms.api.entity.ArcMasterData;

public interface ArcMasterRepository extends CustomMongoRepository<ArcMasterData> {

  ArcMasterData findByMasterLineName(String masterLineName);
}
