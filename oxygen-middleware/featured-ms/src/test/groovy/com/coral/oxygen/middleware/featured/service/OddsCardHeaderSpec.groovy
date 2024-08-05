package com.coral.oxygen.middleware.featured.service

import com.coral.oxygen.middleware.common.service.featured.OddsCardHeader
import com.coral.oxygen.middleware.common.service.OutrightsConfig
import com.coral.oxygen.middleware.common.service.SportsConfig
import com.coral.oxygen.middleware.pojos.model.output.featured.EventsModule
import com.google.gson.Gson
import com.google.gson.GsonBuilder
import org.springframework.core.io.ClassPathResource
import spock.lang.Specification

class OddsCardHeaderSpec extends Specification {
  OddsCardHeader oddsCardHeader
  Gson gson

  def setup() {
    gson = new GsonBuilder().create()
    oddsCardHeader = new OddsCardHeader()
    oddsCardHeader.setOutrightsConfig(new OutrightsConfig())
    oddsCardHeader.setSportsConfig(new SportsConfig(new ClassPathResource("sportsConfig.json"), gson))
  }


  def cleanup() {
    oddsCardHeader = null
  }


  def "Test calculating head titles for output modules"() throws IOException {
    expect:
    EventsModule module = gson.fromJson(new InputStreamReader(new ClassPathResource("oddsCardHeader/" + moduleResourceName)
        .getInputStream()), EventsModule.class)
    List<String> headers = oddsCardHeader.calculateHeadTitles(module.getData())
    expectedHeaders == headers

    where:
    moduleResourceName | expectedHeaders
    "A_module.json" | ["home", "draw", "away"]
    "B_module.json" | ["home", "draw", "away"]
  }
}
