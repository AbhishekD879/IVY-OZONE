package com.ladbrokescoral.oxygen.cms.api.repository;

import com.ladbrokescoral.oxygen.cms.api.entity.TeamKit;
import java.util.List;

public interface TeamKitRepository extends CustomMongoRepository<TeamKit> {

  List<TeamKit> findByBrandAndTeamName(String brand, String teamName);
}
