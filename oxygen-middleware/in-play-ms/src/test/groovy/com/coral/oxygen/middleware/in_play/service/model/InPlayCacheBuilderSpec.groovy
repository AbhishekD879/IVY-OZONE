package com.coral.oxygen.middleware.in_play.service.model


import com.coral.oxygen.middleware.in_play.service.scoreboards.ScoreboardEvent
import com.coral.oxygen.middleware.pojos.model.output.inplay.SportSegment
import com.google.gson.Gson
import com.google.gson.GsonBuilder
import com.google.gson.reflect.TypeToken
import spock.lang.Specification

import java.nio.file.Files
import java.nio.file.Path
import java.nio.file.Paths

class InPlayCacheBuilderSpec extends Specification {

  List<SportSegment> segments;
  Gson gson;

  def setup() {
    gson = new GsonBuilder().create()
    Path resource = Paths.get(ClassLoader.getSystemResource("SportSegmentsOk.json").toURI())
    String source = new String(Files.readAllBytes(resource))
    segments = gson.fromJson(source, new TypeToken<List<SportSegment>>() {}.getType())
    expect:
    18 == segments.size()
  }

  def "verify segments"() {

    given:
    InPlayCache cache = new InPlayCacheBuilder().sportSegments(segments).build()

    expect:
    49 == cache.getSportSegmentCaches().size()

    int count = 1

    when:

    cache.getSportSegmentCaches().sort { c1, c2 -> (c1.getStructuredKey() <=> c2.getStructuredKey()) }
    cache.getSportSegmentCaches().each { sCache ->
      //calculates for parents the number of descendants
      if (sCache.getStructuredKey().getTypeId() == null) {
        final Set<String> counter = new HashSet<>()
        sCache.getSportSegment().getEventsByTypeName().each { ts ->
          counter.add(ts.getTypeId())
        }
        count += counter.size() + 1
      }
    }


    then:
    count == cache.getSportSegmentCaches().size()
  }

  def "verify cache entity types"() {

    given:
    InPlayCache cache = new InPlayCacheBuilder().sportSegments(segments).build()

    expect:
    49 == cache.getSportSegmentCaches().size()

    cache.getSportSegmentCaches().each { sCache ->
      if (sCache.getStructuredKey().getTypeId() == null) {

        then:
        sCache.getSportSegment() != null
      } else {

        then:
        sCache.getModuleDataItem() != null

        and:
        sCache.getModuleDataItem().size() > 0
      }
    }
  }

}
