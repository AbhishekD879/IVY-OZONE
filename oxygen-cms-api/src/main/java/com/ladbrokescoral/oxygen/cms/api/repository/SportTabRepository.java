package com.ladbrokescoral.oxygen.cms.api.repository;

import com.ladbrokescoral.oxygen.cms.api.entity.SportTab;
import java.util.List;
import org.springframework.data.mongodb.repository.Query;

public interface SportTabRepository extends CustomMongoRepository<SportTab> {
  List<SportTab> findAllByBrandAndSportId(String brand, Integer sportId);

  List<SportTab> findAllByBrandAndSportIdOrderBySortOrderAsc(String brand, Integer sportId);

  List<SportTab> findAllByBrandAndSportIdAndName(String brand, Integer sportId, String name);

  List<SportTab> findAllByBrandAndNameAndEnabledTrue(String brand, String tabName);

  List<SportTab> findAllByNameAndCheckEventsTrue(String name);

  @Query(value = "{'brand':?0, 'name':?1, 'enabled':true, 'checkEvents':true}")
  List<SportTab> findActiveWithCheckEventsTrue(String brand, String name);

  List<SportTab> findAllByBrandAndSportIdAndEnabledTrue(String brand, int sportId);

  void deleteByBrandAndSportId(String brand, Integer categoryId);
}
