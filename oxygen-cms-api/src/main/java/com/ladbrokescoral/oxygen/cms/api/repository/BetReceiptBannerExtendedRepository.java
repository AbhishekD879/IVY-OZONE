package com.ladbrokescoral.oxygen.cms.api.repository;

import com.ladbrokescoral.oxygen.cms.api.service.SortableService;
import java.time.Instant;
import java.util.List;
import org.springframework.data.mongodb.core.query.Criteria;
import org.springframework.data.mongodb.core.query.Query;

public interface BetReceiptBannerExtendedRepository<T> {
  List<T> findBetReceiptBanners(String brand);

  default Query createBetReceiptBannerQuery(String brand) {
    Query query = new Query();
    query.addCriteria(
        Criteria.where("disabled")
            .is(false)
            .and("brand")
            .is(brand)
            .and("validityPeriodEnd")
            .gt(Instant.now())
            .and("validityPeriodStart")
            .lt(Instant.now()));
    query.with(SortableService.SORT_BY_SORT_ORDER_ASC);
    return query;
  }
}
