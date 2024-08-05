package com.coral.oxygen.middleware.in_play.service.model;

import static java.util.stream.Collectors.toMap;

import com.coral.oxygen.middleware.pojos.model.output.inplay.SportSegment;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import lombok.extern.slf4j.Slf4j;

@Slf4j
public final class InPlayCacheBuilder {

  private final InPlayCache thisCache;

  private Map<RawIndex, InPlayCache.SportSegmentCache> groupBySelectors;

  public InPlayCacheBuilder() {
    this.thisCache = new InPlayCache();
  }

  private void buildSegmentDistCache(List<SportSegment> sportSegments) {
    this.groupBySelectors =
        sportSegments.stream()
            .collect(
                toMap(
                    sportSegment ->
                        new RawIndex()
                            .categoryId(sportSegment.getCategoryId())
                            .marketSelector(sportSegment.getMarketSelector())
                            .topLevelType(sportSegment.getTopLevelType().toString()),
                    InPlayCache.SportSegmentCache::new));
  }

  public InPlayCacheBuilder sportSegments(List<SportSegment> sportSegments) {
    buildSegmentDistCache(sportSegments);
    sportSegments.forEach(
        segment -> {
          if (segment.getMarketSelectorOptions() != null) {
            segment
                .getMarketSelectorOptions()
                .forEach(
                    market -> {
                      // ${object.categoryId}::${object.topLevelType}::${marketSelector}
                      RawIndex index =
                          new RawIndex()
                              .categoryId(segment.getCategoryId())
                              .topLevelType(segment.getTopLevelType().toString())
                              .marketSelector(market);
                      SportSegment thisSegment = groupBySelectors.get(index).sportSegment;

                      // ${object.categoryId}::${object.topLevelType}::${marketSelector}::${eventByTypeName.typeId}
                      thisSegment
                          .getEventsByTypeName()
                          .forEach(
                              eventByTypeName ->
                                  this.groupBySelectors.put(
                                      new RawIndex()
                                          .categoryId(thisSegment.getCategoryId())
                                          .topLevelType(thisSegment.getTopLevelType().toString())
                                          .marketSelector(market)
                                          .typeId(eventByTypeName.getTypeId()),
                                      new InPlayCache.SportSegmentCache(
                                          eventByTypeName.getEvents())));
                    });
          }
          // ${object.categoryId}::${object.topLevelType}
          // to be check
          // don't need
          // ${object.categoryId}::${object.topLevelType}::${eventByTypeName.typeId}
          segment
              .getEventsByTypeName()
              .forEach(
                  eventByTypeName ->
                      this.groupBySelectors.put(
                          new RawIndex()
                              .categoryId(segment.getCategoryId())
                              .topLevelType(segment.getTopLevelType().toString())
                              .typeId(eventByTypeName.getTypeId()),
                          new InPlayCache.SportSegmentCache(eventByTypeName.getEvents())));
        });
    return this;
  }

  public InPlayCache build() {
    List<InPlayCache.SportSegmentCache> sportSegments = new ArrayList<>();
    this.groupBySelectors.forEach(
        (rawIndex, ssGroup) -> {
          ssGroup.setStructuredKey(rawIndex);
          sportSegments.add(ssGroup);
        });
    if (log.isDebugEnabled()) {
      log.debug(" ========================== new cache ===========================");
      sportSegments.forEach(ss -> log.debug(" new cache for key {}", ss.structuredKey));
    }
    thisCache.setSportSegmentCaches(sportSegments);
    return thisCache;
  }

  /**
   * For help in debug.
   *
   * @param key
   * @return
   */
  public InPlayCache.SportSegmentCache findByKey(String key) {
    return groupBySelectors.get(new RawIndex(key));
  }
}
