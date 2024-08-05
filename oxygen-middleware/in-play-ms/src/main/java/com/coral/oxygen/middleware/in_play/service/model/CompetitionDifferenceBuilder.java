package com.coral.oxygen.middleware.in_play.service.model;

import com.coral.oxygen.middleware.pojos.model.output.inplay.TypeSegment;
import com.newrelic.api.agent.NewRelic;
import java.util.Collection;
import java.util.Collections;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Map;
import java.util.Set;
import java.util.stream.Collectors;
import lombok.AllArgsConstructor;
import lombok.NoArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.util.ObjectUtils;

/**
 * WARNING: DON'T put "IF" here anymore!
 *
 * <p>Exception cases: - when sports segment are empty. - when sports segment have empty type
 * segments, for both sides new one, the old one.
 *
 * <p>If it happened should be checking logic on the down level, instead of put "IF" here. (in
 * InPlayDataConsumer for example).
 *
 * <p>Created by Aliaksei Yarotski on 12/8/17.
 */
@Slf4j
public class CompetitionDifferenceBuilder {

  @NoArgsConstructor
  @AllArgsConstructor
  public static class SegmentsPare<P> {

    P latest;
    P previous;
  }

  private String generation;
  private Map<RawIndex, SportCompetitionChanges> thisChanges;
  private Map<RawIndex, SegmentsPare<Map<String, TypeSegment>>> diffSum;

  private CompetitionDifferenceBuilder() {
    thisChanges = new HashMap<>();
    diffSum = new HashMap<>();
  }

  public CompetitionDifferenceBuilder generation(long generation) {
    this.generation = String.valueOf(generation);
    return this;
  }

  /** Compare sports segment by TypeId */
  private CompetitionDifferenceBuilder addSegments(
      RawIndex index, SegmentsPare<Map<String, TypeSegment>> segments) {
    Map<String, TypeSegment> added = new HashMap<>();
    Set<String> changed = new HashSet<>();
    for (Map.Entry<String, TypeSegment> ts : segments.latest.entrySet()) {
      TypeSegment prevTypeSegment = segments.previous.remove(ts.getKey());
      // check if added new events
      if (prevTypeSegment != null
          && ts.getValue().getEventCount() != prevTypeSegment.getEventCount()) {
        changed.add(ts.getKey());
      } else if (prevTypeSegment == null) {

        added.put(ts.getKey(), ts.getValue().cloneWithEmptyEvents());
      }
    }
    thisChanges.put(
        index,
        new SportCompetitionChanges(
            index.toStructuredKey(), this.generation, added, segments.previous.keySet(), changed));
    return this;
  }

  public Collection<SportCompetitionChanges> build() {
    return thisChanges.values().stream()
        .filter(SportCompetitionChanges::isNotEmpty)
        .collect(Collectors.toSet());
  }

  /** Why the processor is processing empty data?! */
  public CompetitionDifferenceBuilder compareCaches(
      InPlayCache latestCache, InPlayCache previousCache) {
    if (notEmptyCaches(latestCache, previousCache)) {
      compareSportsSegment(latestCache, previousCache);
    } else {
      log.error(
          "Comparing went wrong because latestCache : {} and previousCache : {}",
          latestCache,
          previousCache);
      NewRelic.noticeError("Comparing went wrong because latestCache or previousCache are null");
    }
    return this;
  }

  /** Process Sports segment ( typeId == null ) */
  private void compareSportsSegment(InPlayCache latestCache, InPlayCache previousCache) {
    latestCache
        .getSportSegmentCaches()
        .forEach(
            segmentCache -> {
              RawIndex thisIndex = segmentCache.structuredKey;
              SegmentsPare<Map<String, TypeSegment>> pare;
              if (thisIndex.getTypeId() == null) {
                pare = new SegmentsPare(null, Collections.emptyMap());
                pare.latest =
                    segmentCache.getSportSegment().getEventsByTypeName().stream()
                        .collect(Collectors.toMap((TypeSegment::getTypeId), (ts -> ts)));
                diffSum.put(thisIndex, pare);
              }
            });
    previousCache
        .getSportSegmentCaches()
        .forEach(
            segmentCache -> {
              RawIndex thisIndex = segmentCache.structuredKey;
              SegmentsPare<Map<String, TypeSegment>> pare;
              if (thisIndex.getTypeId() == null) {
                pare =
                    diffSum.getOrDefault(thisIndex, new SegmentsPare(Collections.emptyMap(), null));
                pare.previous =
                    segmentCache.getSportSegment().getEventsByTypeName().stream()
                        .collect(Collectors.toMap((TypeSegment::getTypeId), (ts -> ts)));
                diffSum.put(thisIndex, pare);
              }
            });
    diffSum
        .entrySet()
        .forEach(
            e -> {
              log.debug("the following node will be processed: {}", e.getKey().toStructuredKey());
              addSegments(e.getKey(), e.getValue());
            });
  }

  public boolean notEmptyCaches(InPlayCache latestCache, InPlayCache previousCache) {
    return !ObjectUtils.isEmpty(latestCache)
        && !ObjectUtils.isEmpty(latestCache.getSportSegmentCaches())
        && !ObjectUtils.isEmpty(previousCache)
        && !ObjectUtils.isEmpty(previousCache.getSportSegmentCaches());
  }

  public static CompetitionDifferenceBuilder builder() {
    return new CompetitionDifferenceBuilder();
  }
}
