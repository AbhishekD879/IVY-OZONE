package com.ladbrokescoral.oxygen.cms.api.repository;

import com.ladbrokescoral.oxygen.cms.api.entity.SurfaceBet;
import java.util.List;
import org.springframework.data.mongodb.repository.Query;
import org.springframework.stereotype.Repository;

@Repository
public interface SurfaceBetMongoRepository extends CustomMongoRepository<SurfaceBet> {

  @Query(value = "{references: {$elemMatch: {'relatedTo':?0, 'refId': ?1}}}")
  List<SurfaceBet> findTheMaxSortOrderOfThePage(String sportType, String pageId);
}
