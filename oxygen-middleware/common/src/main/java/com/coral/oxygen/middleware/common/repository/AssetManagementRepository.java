package com.coral.oxygen.middleware.common.repository;

import com.coral.oxygen.middleware.pojos.model.output.AssetManagement;
import java.util.List;
import java.util.Optional;
import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface AssetManagementRepository extends CrudRepository<AssetManagement, String> {

  public Optional<AssetManagement> findByTeamNameIgnoreCaseAndSportId(
      String teamName, Integer sportId);

  public List<AssetManagement> findBySportId(Integer sportId);
}
