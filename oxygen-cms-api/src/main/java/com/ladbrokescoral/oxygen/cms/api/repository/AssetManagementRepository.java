package com.ladbrokescoral.oxygen.cms.api.repository;

import com.ladbrokescoral.oxygen.cms.api.entity.AssetManagement;
import java.util.List;
import java.util.Optional;

public interface AssetManagementRepository extends CustomMongoRepository<AssetManagement> {
  List<AssetManagement> findAllByBrand(String brand);

  Optional<AssetManagement> findByTeamNameAndSportIdAndBrand(
      String teamName, Integer sportId, String brand);

  List<AssetManagement> findByIdIn(List<String> amIds);
}
