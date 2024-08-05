package com.ladbrokescoral.oxygen.cms.api.repository;

import com.ladbrokescoral.oxygen.cms.api.entity.PageType;
import com.ladbrokescoral.oxygen.cms.api.entity.SportQuickLink;
import java.time.Instant;
import java.util.List;
import org.springframework.data.mongodb.repository.Query;

public interface SportQuickLinkRepository
    extends CustomSegmentRepository<SportQuickLink>, FindByRepository<SportQuickLink> {

  List<SportQuickLink> findAllByBrandAndPageIdOrderBySortOrderAsc(String brand, String sportId);

  List<SportQuickLink> findAllByBrandAndPageTypeAndPageIdOrderBySortOrderAsc(
      String brand, PageType pageType, String pageId);

  void deleteAllByBrandAndPageTypeAndPageId(String brand, PageType pageType, String pageId);

  @Query(
      "{"
          + "'_id': {'$ne':?0},"
          + "'validityPeriodStart': {'$lte': ?1}, "
          + "'validityPeriodEnd': {'$gte': ?1}, "
          + "'disabled': false,"
          + "'pageId':'0'"
          + "'brand': ?2"
          + "}")
  List<SportQuickLink> findAllActiveAndvalidityPeriodStartIsAfterAndvalidityPeriodEndIsBefore(
      String id, Instant now, String brand);

  List<SportQuickLink> findAllByBrandAndPageTypeIn(String brand, List<PageType> pageTypes);
}
