package com.coral.oxygen.middleware.in_play.service.model


import com.coral.oxygen.middleware.in_play.service.model.CompetitionDifferenceBuilder.SegmentsPare
import com.coral.oxygen.middleware.pojos.model.output.inplay.SportSegment
import com.coral.oxygen.middleware.pojos.model.output.inplay.TypeSegment
import spock.lang.Specification

class CompetitionDifferenceBuilderSpec extends Specification {


  def "matrix of cache comparing"() {
    setup:
    def dataInput = createDummyCache(key, typeId, newCount, prevCount)

    expect:
    Collection<SportCompetitionChanges> diff = CompetitionDifferenceBuilder.builder()
        .compareCaches(dataInput.latest, dataInput.previous).build()
    added == wasAdded(diff)
    changed == wasChanged(diff)
    removed == wasRemoved(diff)

    where:
    key              || typeId || newCount || prevCount || added || changed || removed
    "16::LIVE_EVENT" || "442"  || 1        || null      || "442" || null    || null
    "16::LIVE_EVENT" || "442"  || 2        || 1         || null  || "442"   || null
    "16::LIVE_EVENT" || "442"  || null     || 1         || null  || null    || "442"
    "16::LIVE_EVENT" || "442"  || 1        || 1         || null  || null    || null
    "16::LIVE_EVENT" || "442"  || 1        || 2         || null  || "442"   || null
  }

  String wasAdded(Collection<SportCompetitionChanges> diff) {
    if (diff != null && diff.size() == 1 && diff[0].added != null && diff[0].added.size() == 1) {
      return diff[0].added.values()[0].typeId
    }
    return null
  }

  String wasChanged(Collection<SportCompetitionChanges> diff) {
    if (diff != null && diff.size() == 1 && diff[0].changed != null && diff[0].changed.size() == 1) {
      return diff[0].changed[0]
    }
    return null
  }

  String wasRemoved(Collection<SportCompetitionChanges> diff) {
    if (diff != null && diff.size() == 1 && diff[0].removed != null && diff[0].removed.size() == 1) {
      return diff[0].removed[0]
    }
    return null
  }

  List<TypeSegment> createTypeSegment(String typeId, Integer eventCount) {
    if (eventCount == null) {
      return new ArrayList();
    }
    TypeSegment ts = new TypeSegment();
    ts.setTypeId(typeId);
    ts.setEventCount(eventCount);
    return Arrays.asList(ts);
  }

  SportSegment createSportSegment(String typeId, Integer eventCount) {
    SportSegment sportSegment = new SportSegment();
    sportSegment.eventsByTypeName = createTypeSegment(typeId, eventCount)
    return sportSegment
  }

  List<InPlayCache.SportSegmentCache> createSportSegmentCache(key, typeId, count) {
    InPlayCache.SportSegmentCache ssc = new InPlayCache.SportSegmentCache(createSportSegment(typeId, count), null, new RawIndex(key))
    return Arrays.asList(ssc)
  }

  SegmentsPare<InPlayCache> createDummyCache(key, typeId, newCount, prevCount) {
    InPlayCache newCache = new InPlayCache(createSportSegmentCache(key, typeId, newCount))
    InPlayCache prevCache = new InPlayCache(createSportSegmentCache(key, typeId, prevCount))
    return new SegmentsPare<InPlayCache>(newCache, prevCache)
  }
}
