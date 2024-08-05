package com.oxygen.publisher.service.impl

import com.oxygen.publisher.inplay.InplayServiceRegistry
import com.oxygen.publisher.inplay.service.InplayConsumerApi
import com.oxygen.publisher.inplay.service.InplayDataServiceImpl
import com.oxygen.publisher.model.InPlayCache
import com.oxygen.publisher.model.InPlayData
import com.oxygen.publisher.model.SportSegment
import com.oxygen.publisher.model.SportsRibbon
import com.oxygen.publisher.model.VirtualSportEvents
import retrofit2.Call
import retrofit2.Response
import spock.lang.Specification

class InplayDataServiceImplSpec extends Specification {
  InplayDataServiceImpl inplayDataService

  InplayConsumerApi inplayConsumerApi
  InplayServiceRegistry serviceRegistry
  Call call

  static final String VERSION = "11"

  def setup() {
    inplayConsumerApi = Mock(InplayConsumerApi)
    serviceRegistry = Mock(InplayServiceRegistry)
    call = Mock(Call)

    serviceRegistry.getInplayConsumerApi() >> inplayConsumerApi

    inplayConsumerApi.getVersion() >> call
    inplayConsumerApi.getInPlayModel(VERSION) >> call
    inplayConsumerApi.getSportsRibbon(VERSION) >> call
    inplayConsumerApi.getSportSegment(VERSION) >> call
    inplayConsumerApi.getInPlayCache(VERSION) >> call
    inplayConsumerApi.getVirtualSports(VERSION) >> call


    inplayDataService = Spy(InplayDataServiceImpl)
    inplayDataService.setServiceRegistry(serviceRegistry);
  }

  def "Get last generation calls Api.getVersion inside"() throws IOException {
    call.execute() >> Response.success(VERSION)

    when:
    inplayDataService.getLastGeneration({ r -> assert r == VERSION });

    then:
    1 * inplayConsumerApi.getVersion() >> call
  }

  def "Get in-play model gets the same model that call returns"() throws IOException {
    InPlayData model = new InPlayData()
    call.execute() >> Response.success(model)

    when:
    inplayDataService.getInPlayModel(VERSION, { r -> assert r.is(model) });

    then:
    noExceptionThrown()
  }

  def "Get in-play model gets the same sportsRibbon that call returns"() throws IOException {
    SportsRibbon sportsRibbon = new SportsRibbon()
    call.execute() >> Response.success(sportsRibbon)

    when:
    inplayDataService.getSportsRibbon(VERSION, { r -> assert r.is(sportsRibbon) })

    then:
    noExceptionThrown()
  }

  def "Get in-play model gets the same inPlayCache that call returns"() throws IOException {
    InPlayCache inPlayCache = new InPlayCache()
    call.execute() >> Response.success(inPlayCache)

    when:
    inplayDataService.getInPlayCache(VERSION, { r -> assert r.is(inPlayCache) });

    then:
    noExceptionThrown()
  }

  def "Get in-play model gets the same sportSegment that call returns"() throws IOException {
    SportSegment sportSegment = new SportSegment()
    call.execute() >> Response.success(sportSegment)

    when:
    inplayDataService.getSportSegment(VERSION, { r -> assert r.is(sportSegment) })

    then:
    noExceptionThrown()
  }

  def "Get virtual sports data that call returns"() throws IOException {
    List< VirtualSportEvents> virtualSportEvents = new ArrayList<>();
    call.execute() >> Response.success(virtualSportEvents)

    when:
    inplayDataService.getVirtualSport(VERSION,{r-> assert  r.is(virtualSportEvents)})


    then:
    noExceptionThrown()
  }
}
