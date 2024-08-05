package com.ladbrokescoral.oxygen.cms.api.repository;

import com.ladbrokescoral.oxygen.cms.api.entity.Banner;
import java.time.Instant;
import java.util.List;
import org.bson.types.ObjectId;

public interface BannerRepository extends CustomMongoRepository<Banner> {

  List<Banner>
      findAllByBrandAndDisabledAndCategoryIdInAndValidityPeriodStartBeforeAndValidityPeriodEndAfterOrderBySortOrder(
          String brand,
          Boolean disabled,
          List<ObjectId> categoriesIds,
          Instant validityPeriodStart,
          Instant validityPeriodEnd);
}
