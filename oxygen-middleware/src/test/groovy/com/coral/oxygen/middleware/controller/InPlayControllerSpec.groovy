package com.coral.oxygen.middleware.controller

import com.coral.oxygen.middleware.common.service.ModuleAdapter
import com.coral.oxygen.middleware.in_play.service.InPlayStorageService
import com.coral.oxygen.middleware.pojos.model.output.inplay.SportSegment
import com.google.gson.Gson
import com.google.gson.GsonBuilder
import com.google.gson.reflect.TypeToken
import org.springframework.http.HttpStatus
import org.springframework.http.MediaType
import org.springframework.test.web.servlet.MockMvc
import org.springframework.test.web.servlet.setup.MockMvcBuilders
import spock.lang.Specification

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get

class InPlayControllerSpec extends Specification {

  InPlayStorageService storageService = Mock()
  Gson gson = new GsonBuilder().create()

  InPlayController controller = new InPlayController(storageService, gson)

  MockMvc mockMvc = MockMvcBuilders.standaloneSetup(controller).build()

  def "Get featured data model"() {
    given:
    def latestInPlayData = "Latest InPlay data"
    storageService.getLatestInPlayData() >> latestInPlayData

    when:
    def response = mockMvc.perform(get("/api/debug/inplay")).andReturn().getResponse()
    def content = response.getContentAsString()

    then:
    response.getStatus() == HttpStatus.OK.value()
    response.getContentType().contains(MediaType.TEXT_PLAIN_VALUE)
    content == latestInPlayData
  }

  def "Get latest sport Ribbon"() {
    given:
    def latestSportRibbon = "Latest Sports Ribbon"
    storageService.getLatestSportsRibbon() >> latestSportRibbon

    when:
    def response = mockMvc.perform(get("/api/debug/inplay/LatestSportsRibbon")).andReturn().getResponse()
    def content = response.getContentAsString()

    then:
    response.getStatus() == HttpStatus.OK.value()
    response.getContentType().contains(MediaType.TEXT_PLAIN_VALUE)
    content == latestSportRibbon
  }

  def "Get latest sport Segment"() {
    given:
    def latestSportSegment = "Latest Sports Segment"
    def key = "key"
    storageService.getLatestSportSegment(key) >> latestSportSegment

    when:
    def response = mockMvc.perform(get("/api/debug/inplay/LatestSportSegment").param("key", key)).andReturn().getResponse()
    def content = response.getContentAsString()

    then:
    response.getStatus() == HttpStatus.OK.value()
    response.getContentType().contains(MediaType.TEXT_PLAIN_VALUE)
    content == latestSportSegment
  }

  def "Get All sport segments"() {
    given:
    def sS1 = new SportSegment()
    sS1.setCategoryId(1)
    sS1.setCategoryName("category1")
    def sS2 = new SportSegment()
    sS2.setCategoryId(2)
    sS2.setCategoryName("category2")
    List<SportSegment> sportSegments = Arrays.asList(sS1, sS2)
    storageService.getLatestSportSegmentsObjects() >> sportSegments

    when:
    def response = mockMvc.perform(get("/api/debug/inplay/AllLastSportSegmets")).andReturn().getResponse()
    List<SportSegment> content = ModuleAdapter.FEATURED_GSON.fromJson(response.getContentAsString(),
        new TypeToken<List<SportSegment>>() {}.getType())

    then:
    response.getStatus() == HttpStatus.OK.value()
    response.getContentType().contains(MediaType.TEXT_PLAIN_VALUE)
    content.size() == 2
    for (int i = 0; i < content.size(); ++i) {

      SportSegment segment = content.get(i)
      def categoryCountNumber = i + 1
      segment.getCategoryId() == categoryCountNumber
      segment.getCategoryName().contains(String.format("category%d", categoryCountNumber))
    }
  }
}
