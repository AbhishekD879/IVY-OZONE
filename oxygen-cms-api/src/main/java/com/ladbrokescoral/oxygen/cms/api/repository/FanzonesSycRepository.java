package com.ladbrokescoral.oxygen.cms.api.repository;

import com.ladbrokescoral.oxygen.cms.api.entity.FanzoneSyc;
import java.util.Optional;
import org.springframework.data.mongodb.repository.Query;

public interface FanzonesSycRepository extends CustomMongoRepository<FanzoneSyc> {

  Optional<FanzoneSyc> findByPageName(String pageName);

  void deleteByPageName(String pageName);

  @Query("{'brand': ?0,'pageName': ?1,'?2': ?3}")
  Optional<FanzoneSyc> findByBrandPageNameAndColumn(
      String brand, String pageName, String column, String val);

  @Query("{'brand': ?0,'pageName': ?1}")
  Optional<FanzoneSyc> findAllByBrandAndPageName(String brand, String pageName);
}
