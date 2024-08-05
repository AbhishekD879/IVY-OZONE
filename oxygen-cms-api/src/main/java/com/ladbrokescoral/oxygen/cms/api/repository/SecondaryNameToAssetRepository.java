package com.ladbrokescoral.oxygen.cms.api.repository;

import com.ladbrokescoral.oxygen.cms.api.entity.SecondaryNameToAssetManagement;
import java.util.List;
import java.util.Optional;

public interface SecondaryNameToAssetRepository
    extends CustomMongoRepository<SecondaryNameToAssetManagement> {

  Optional<SecondaryNameToAssetManagement> findByTeamNameAndSportIdAndBrand(
      String teamName, Integer sportId, String brand);

  List<SecondaryNameToAssetManagement> findAllByAssetId(String assetId);

  void deleteAllByAssetId(String assetId);
}
