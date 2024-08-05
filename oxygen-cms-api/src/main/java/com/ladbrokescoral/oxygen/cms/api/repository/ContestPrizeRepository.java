package com.ladbrokescoral.oxygen.cms.api.repository;

import com.ladbrokescoral.oxygen.cms.api.entity.ContestPrize;
import java.util.List;

/** Contest Prizes Repository */
public interface ContestPrizeRepository extends CustomMongoRepository<ContestPrize> {

  List<ContestPrize> findByContestId(String contestId);

  List<ContestPrize> findByBrand(String brand);

  List<ContestPrize> findOneByIdAndAndBrand(String id, String brand);

  List<ContestPrize> deleteByContestId(String contestId);
}
