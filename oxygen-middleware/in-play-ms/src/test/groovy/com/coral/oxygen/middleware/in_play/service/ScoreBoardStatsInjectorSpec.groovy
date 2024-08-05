package com.coral.oxygen.middleware.in_play.service

import com.coral.oxygen.middleware.in_play.service.injector.ScoreBoardStatsInjector
import com.coral.oxygen.middleware.in_play.service.scoreboards.ScoreboardCache
import com.coral.oxygen.middleware.in_play.service.scoreboards.ScoreboardEvent
import com.coral.oxygen.middleware.pojos.model.output.EventsModuleData
import com.coral.oxygen.middleware.pojos.model.output.inplay.InPlayData
import com.coral.oxygen.middleware.pojos.model.output.inplay.InPlayModel
import com.coral.oxygen.middleware.pojos.model.output.inplay.SportSegment
import com.coral.oxygen.middleware.pojos.model.output.inplay.TypeSegment
import com.egalacoral.spark.liveserver.utils.JsonMapper
import com.fasterxml.jackson.annotation.JsonInclude
import com.fasterxml.jackson.databind.DeserializationFeature
import com.fasterxml.jackson.databind.ObjectMapper
import spock.lang.Specification

import java.text.SimpleDateFormat

class ScoreBoardStatsInjectorSpec extends Specification{

  ScoreBoardStatsInjector scoreBoardStatsInjector

  ScoreboardCache scoreboardCache = Mock()

  JsonMapper jsonMapper

  List<Integer> supportedCategories

  def setup() {
    jsonMapper = jsonMapper()
    supportedCategories = List.of(16);
    scoreBoardStatsInjector = new ScoreBoardStatsInjector(supportedCategories,scoreboardCache,jsonMapper)
  }

  def "testScoreBoardStatsInjector"(){
    given:
    def inplayData = buildInplayData(112233,16,"FOOTBALL")
    def json = TestTools.getResourceByPath("Df/footballScoreboard.json")
    def scoreBoardEvent = new ScoreboardEvent("112233",json)
    def se = Optional.of(scoreBoardEvent)
    scoreboardCache.findById(*_) >> se
    when:
    scoreBoardStatsInjector.injectData(inplayData)
    then:
    EventsModuleData moduleData = inplayData.getLivenow().getSportEvents().get(0).getEventsByTypeName().get(0).getEvents().get(0)
    moduleData!=null
    moduleData.getScoreBoardStats()==null
  }

  def "testScoreBoardStatsInjectorWithEmptyStats" () {
    given:
    def inplayData = buildInplayData(112233,16,"FOOTBALL")
    def se = Optional.empty()
    scoreboardCache.findById(*_) >> se
    when:
    scoreBoardStatsInjector.injectData(inplayData)
    then:
    EventsModuleData moduleData = inplayData.getLivenow().getSportEvents().get(0).getEventsByTypeName().get(0).getEvents().get(0)
    moduleData!=null
    moduleData.getScoreBoardStats()==null
  }

  def "testScoreBoardStatsInjectorForOtherSportsThanFootball" () {
    given:
    def inplayData = buildInplayData(112233,21,"HORSE RACING")
    when:
    scoreBoardStatsInjector.injectData(inplayData)
    then:
    0 * scoreboardCache.findById(*_)
    EventsModuleData moduleData = inplayData.getLivenow().getSportEvents().get(0).getEventsByTypeName().get(0).getEvents().get(0)
    moduleData!=null
    moduleData.getScoreBoardStats()==null
  }


  JsonMapper jsonMapper() {
    ObjectMapper mapper = new ObjectMapper()
    mapper.setSerializationInclusion(JsonInclude.Include.NON_NULL)
    mapper.configure(DeserializationFeature.FAIL_ON_UNKNOWN_PROPERTIES, false)
    mapper.setDateFormat(new SimpleDateFormat("MMM dd, YYYY h:MM:ss a"))
    return new JsonMapper(mapper)
  }

  InPlayData buildInplayData(Integer eventId, Integer categoryId, String categoryCode) {

    InPlayModel livenow = new InPlayModel()
    SportSegment segment = new SportSegment()
    segment.setCategoryId(categoryId)
    segment.setCategoryCode(categoryCode)
    TypeSegment typeSegment = new TypeSegment()
    EventsModuleData moduleData = new EventsModuleData()
    moduleData.setId(eventId)
    typeSegment.getEvents().add(moduleData)
    segment.getEventsByTypeName().add(typeSegment)
    livenow.getSportEvents().add(segment)
    return new InPlayData(livenow,new InPlayModel(),new InPlayModel(),new InPlayModel())
  }
}
