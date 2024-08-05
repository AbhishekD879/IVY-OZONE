package com.coral.oxygen.middleware.in_play.service

import com.coral.oxygen.middleware.common.service.SportsConfig
import com.coral.oxygen.middleware.in_play.service.injector.SportsConfigDataInjector
import com.coral.oxygen.middleware.pojos.model.output.inplay.InPlayData
import org.springframework.core.io.ClassPathResource
import spock.lang.Specification

class SportsConfigDataInjectorSpec extends Specification {
  SportsConfigDataInjector dataInjector

  def setup() {
    ClassPathResource sportsConfigFile = new ClassPathResource("SportsConfigDataInjectorTest/sportsConfig.json")
    dataInjector = new SportsConfigDataInjector(new SportsConfig(sportsConfigFile, TestTools.GSON))
  }

  def "Test sports config data injection"() {
    InPlayData data = TestTools.inPlayDataFromFile("SportsConfigDataInjectorTest/inputData.json")

    when:
    dataInjector.injectData(data)

    then:
    "football" == data.getLivenow().getSportEvents().get(0).getCategoryPath()
    data.getLivenow().getSportEvents().get(1).getCategoryPath() == null
    "tennis" == data.getUpcoming().getSportEvents().get(0).getCategoryPath()
    "someOldValue" == data.getUpcoming().getSportEvents().get(1).getCategoryPath()
  }
}
