package com.ladbrokescoral.oxygen.cms.api.repository;

import com.ladbrokescoral.oxygen.cms.api.entity.BybWidgetData;
import java.time.Instant;
import java.util.List;
import java.util.Optional;
import org.springframework.data.domain.Sort;
import org.springframework.data.mongodb.repository.Query;

public interface BybWidgetDataRepository extends CustomMongoRepository<BybWidgetData> {

  @Query("{ brand : ?0,'displayFrom':{'$lte':?1},'displayTo':{'$gte':?1} }")
  List<BybWidgetData> findActiveRecordsByBrand(String brand, Instant now);

  @Query("{ brand : ?0,'displayTo':{'$lt':?1} }")
  List<BybWidgetData> findExpiredRecordsByBrandOrderBySortOrderAsc(
      String brand, Instant now, Sort sortBySortOrderAsc);

  @Query("{ brand : ?0,'displayFrom':{'$gt':?1} }")
  List<BybWidgetData> findFutureRecordsByBrand(String brand, Instant now);

  @Query("{ brand : ?0,'displayTo':{'$gte':?1} }")
  List<BybWidgetData> findActiveAndFutureRecordsByBrandOrderBySortOrderAsc(
      String brand, Instant now, Sort sortBySortOrderAsc);

  @Query("{ brand : ?0,'displayFrom':{'$lt':?1},'displayTo':{'$gte':?1} }")
  List<BybWidgetData> findActiveRecordsByBrandOrderBySortOrderAsc(
      String brand, Instant now, Sort sortBySortOrderAsc);

  Optional<BybWidgetData> findByMarketId(String marketId);
}
