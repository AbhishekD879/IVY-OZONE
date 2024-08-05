package com.ladbrokescoral.oxygen.cms.api.repository;

import com.ladbrokescoral.oxygen.cms.api.entity.PopularAccaWidgetData;
import java.time.Instant;
import java.util.List;
import org.springframework.data.domain.Sort;
import org.springframework.data.mongodb.repository.Query;

public interface PopularAccaWidgetDataRepository
    extends CustomMongoRepository<PopularAccaWidgetData> {

  @Query("{ brand : ?0,'displayFrom':{'$lte':?1},'displayTo':{'$gte':?1} }")
  List<PopularAccaWidgetData> findActiveRecordsByBrand(String brand, Instant now);

  @Query("{ brand : ?0,'displayTo':{'$lt':?1} }")
  List<PopularAccaWidgetData> findExpiredRecordsByBrandOrderBySortOrderAsc(
      String brand, Instant now, Sort sortBySortOrderAsc);

  @Query("{ brand : ?0,'displayFrom':{'$gt':?1} }")
  List<PopularAccaWidgetData> findFutureRecordsByBrand(String brand, Instant now);

  @Query("{ brand : ?0,'displayTo':{'$gte':?1} }")
  List<PopularAccaWidgetData> findActiveAndFutureRecordsByBrandOrderBySortOrderAsc(
      String brand, Instant now, Sort sortBySortOrderAsc);

  @Query("{ brand : ?0,'displayFrom':{'$lt':?1},'displayTo':{'$gte':?1} }")
  List<PopularAccaWidgetData> findActiveRecordsByBrandOrderBySortOrderAsc(
      String brand, Instant now, Sort sortBySortOrderAsc);
}
