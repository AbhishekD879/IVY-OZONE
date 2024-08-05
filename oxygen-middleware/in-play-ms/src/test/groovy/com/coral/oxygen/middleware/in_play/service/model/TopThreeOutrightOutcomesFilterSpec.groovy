package com.coral.oxygen.middleware.in_play.service.model

import com.coral.oxygen.middleware.in_play.service.TopThreeOutrightOutcomesFilter
import com.egalacoral.spark.siteserver.model.Event
import com.google.gson.Gson
import com.google.gson.GsonBuilder
import spock.lang.Specification

class TopThreeOutrightOutcomesFilterSpec extends Specification {

  TopThreeOutrightOutcomesFilter filter
  final static Gson GSON = new GsonBuilder().create()

  def setup() {
    filter = new TopThreeOutrightOutcomesFilter()
  }

  def "Check TopThreeOutrightOutcomesFilter"() {
    setup:
    List<Event> events = Collections.singletonList(GSON.fromJson(new InputStreamReader(this.class.getClassLoader()
        .getResourceAsStream("OutrightOutcomesFilterTest/outrightEvent.json")), Event.class))

    expect:
    6 == events.get(0).getMarkets().get(0).getOutcomes().size()

    when:
    filter.filterOutcomes(events)

    then:
    3 == events.get(0).getMarkets().get(0).getOutcomes().size()
    "488774695" == events.get(0).getMarkets().get(0).getOutcomes().get(0).getId()
    "488774694" == events.get(0).getMarkets().get(0).getOutcomes().get(1).getId()
    "488774698" == events.get(0).getMarkets().get(0).getOutcomes().get(2).getId()
  }
}
