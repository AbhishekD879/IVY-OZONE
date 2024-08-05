package com.ladbrokescoral.oxygen.cms.api.repository;

import com.ladbrokescoral.oxygen.cms.api.entity.HighlightCarousel;
import com.ladbrokescoral.oxygen.cms.api.entity.PageType;
import java.time.Instant;
import java.util.List;
import org.springframework.data.mongodb.repository.Query;

public interface HighlightCarouselRepository extends CustomSegmentRepository<HighlightCarousel> {
  List<HighlightCarousel> findByBrandAndPageTypeAndPageIdOrderBySortOrderAsc(
      String brand, PageType pageType, String sport);

  List<HighlightCarousel>
      findByBrandAndDisplayFromIsBeforeAndDisplayToIsAfterAndDisabledIsFalseOrderBySortOrderAsc(
          String brand, Instant displayFrom, Instant displayTo);

  void deleteAllByBrandAndPageTypeAndPageId(String brand, PageType pageType, String pageId);

  @Query("{$and:[{'typeId':?0},{'brand' : ?1},{'pageId' : ?3},{'pageType': ?2}]}")
  List<HighlightCarousel> findByTypeIdAndBrandAndPageTypeAndPageId(
      Integer typeId, String brand, PageType pageType, String sport);

  @Query("{$and:[{'events':{'$in' : [?0]}},{'brand' : ?1},{'pageId' : ?3},{'pageType': ?2}]}")
  List<HighlightCarousel> findByEventIdAndBrandAndPageTypeAndPageId(
      String eventId, String brand, PageType sport, String pageId);
}
