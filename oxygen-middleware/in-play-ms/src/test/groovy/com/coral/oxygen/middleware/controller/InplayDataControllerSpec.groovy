package com.coral.oxygen.middleware.controller

import com.coral.oxygen.middleware.in_play.service.InplayDataService
import com.coral.oxygen.middleware.in_play.service.model.InPlayCache
import com.coral.oxygen.middleware.pojos.model.cms.VirtualSportEvents
import com.coral.oxygen.middleware.pojos.model.output.inplay.InPlayData
import com.coral.oxygen.middleware.pojos.model.output.inplay.SportSegment
import com.coral.oxygen.middleware.pojos.model.output.inplay.SportsRibbon
import com.coral.oxygen.middleware.pojos.model.output.inplay.SportsRibbonItem
import com.google.gson.Gson
import org.springframework.http.HttpStatus
import org.springframework.http.MediaType
import org.springframework.test.web.servlet.MockMvc
import org.springframework.test.web.servlet.setup.MockMvcBuilders
import spock.lang.Specification

import java.time.Instant

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get

class InplayDataControllerSpec extends Specification {

  InplayDataService service = Mock()

  InplayDataController controller = new InplayDataController(service)

  MockMvc mockMvc = MockMvcBuilders.standaloneSetup(controller).build()

  static final long instantTime = Instant.now().toEpochMilli()

  def "Check generation"() {
    given:
    service.getGeneration() >> "testGen"

    when:
    def mock = mockMvc.perform(get("/api/inplay/generation")).andReturn().getResponse()

    then:
    mock.getStatus() == HttpStatus.OK.value()
    "testGen" == mock.getContentAsString()
  }

  def "Check InPlayData"() {
    given:
    def actual = new InPlayData()
    actual.setCreationTime(instantTime)
    service.getInPlayModel("test-1") >> actual

    when:
    def mock = mockMvc.perform(get("/api/inplay/model/{version}", "test-1")).andReturn().getResponse()

    InPlayData expected = new Gson().fromJson(mock.getContentAsString(), InPlayData.class)

    then:
    mock.getStatus() == HttpStatus.OK.value()
    mock.getContentType() == MediaType.APPLICATION_JSON_VALUE
    expected.getGeneration() == actual.getGeneration()
    expected.getCreationTime() == actual.getCreationTime()
  }

  def "Check SportsRibbon"() {
    given:
    def actual = new SportsRibbon()
    def sportRibbonItem = new SportsRibbonItem()
    sportRibbonItem.setCategoryId(1)
    actual.setItems(Arrays.asList(sportRibbonItem))

    service.getSportsRibbon(_) >> actual

    when:
    def mock = mockMvc.perform(get("/api/inplay/sportsribbon/{version}", "test-1")).andReturn().getResponse()

    SportsRibbon expected = new Gson().fromJson(mock.getContentAsString(), SportsRibbon.class)

    then:
    mock.getStatus() == HttpStatus.OK.value()
    mock.getContentType() == MediaType.APPLICATION_JSON_VALUE
    expected.getItems() != null
    expected.getItems().size() == actual.getItems().size()
    expected.getItems().get(0).getCategoryId() == actual.getItems().get(0).getCategoryId()
  }

  def "Check InplayCache"() {
    given:
    def sportSegment = new SportSegment()
    sportSegment.setCategoryId(1)
    def sportSegmentCache = new InPlayCache.SportSegmentCache(sportSegment)
    def actual = new InPlayCache()
    List<InPlayCache.SportSegmentCache> cacheList = new ArrayList<>()
    cacheList.add(sportSegmentCache)
    actual.setSportSegmentCaches(cacheList)

    service.getInPlayCache(_) >> actual

    when:
    def mock = mockMvc.perform(get("/api/inplay/cache/{version}", "test-1")).andReturn().getResponse()

    InPlayCache expected = new Gson().fromJson(mock.getContentAsString(), InPlayCache.class)

    then:
    mock.getStatus() == HttpStatus.OK.value()
    mock.getContentType() == MediaType.APPLICATION_JSON_VALUE
    expected != null
    expected.getSportSegmentCaches() != null
    expected.getSportSegmentCaches().size() == actual.getSportSegmentCaches().size()
    expected.getSportSegmentCaches().get(0).getSportSegment().getCategoryId() == actual.getSportSegmentCaches().get(0).getSportSegment().getCategoryId()
  }

  def "Check SportSegments"() {
    given:
    def actual = new SportSegment()
    actual.setCategoryId(1)

    service.getSportSegment(_) >> actual

    when:
    def mock = mockMvc.perform(get("/api/inplay/sportsegment/{storageKey}", "test-1")).andReturn().getResponse()

    SportSegment expected = new Gson().fromJson(mock.getContentAsString(), SportSegment.class)

    then:
    mock.getStatus() == HttpStatus.OK.value()
    mock.getContentType() == MediaType.APPLICATION_JSON_VALUE
    expected != null
    expected.getCategoryId() == actual.getCategoryId()
  }
  def "Check Virtual Sports Data"() {
    given:
    List< VirtualSportEvents> list = new ArrayList<>()
    VirtualSportEvents vs = new VirtualSportEvents("Cricket",3)
    list.add(vs)

    service.getVirtualSportData(_) >> list

    when:
    def mock = mockMvc.perform(get("/api/inplay/virtuals/{storageKey}", "test-1")).andReturn().getResponse()

    List<VirtualSportEvents> expected = new Gson().fromJson(mock.getContentAsString(),List.class)

    then:
    mock.getStatus() == HttpStatus.OK.value()
    mock.getContentType() == MediaType.APPLICATION_JSON_VALUE
    mock != null
    list.size() == expected.size()
  }
}
