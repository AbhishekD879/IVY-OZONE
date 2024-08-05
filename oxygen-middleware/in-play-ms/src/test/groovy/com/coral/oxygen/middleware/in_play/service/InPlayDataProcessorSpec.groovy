package com.coral.oxygen.middleware.in_play.service

import com.coral.oxygen.middleware.common.service.notification.MessagePublisher
import com.coral.oxygen.middleware.common.service.notification.topic.TopicType
import com.coral.oxygen.middleware.in_play.service.config.InPlayDataProcessorConfig
import com.coral.oxygen.middleware.in_play.service.market.selector.MarketSelectorService
import com.coral.oxygen.middleware.pojos.model.output.inplay.InPlayData
import com.coral.oxygen.middleware.pojos.model.output.inplay.SportSegment
import com.coral.oxygen.middleware.pojos.model.output.inplay.SportsRibbon
import spock.lang.Specification

class InPlayDataProcessorSpec extends Specification {

  InPlayDataProcessor dataProcessor
  InPlayDataConsumer consumer = Mock()
  InPlayStorageService storageService = Mock()
  MessagePublisher messagePublisher = Mock()
  InplayLiveServerSubscriber inplayLiveServerSubscriber = Mock()
  InPlayDataSorter inPlayDataSorter = Mock()
  InPlayDataProcessorConfig.InPlayDataProcessorBuilder builder = Mock()

  def setup() {
    builder.getStorageService() >> storageService
    builder.getMessagePublisher() >> messagePublisher
    builder.getConsumer() >> consumer
    builder.getGson() >> TestTools.GSON
    builder.getInplayLiveServerSubscriber() >> inplayLiveServerSubscriber
    builder.getMarketSelectorService() >> new MarketSelectorService(TestTools.GSON)
    builder.getInPlayDataSorter() >> inPlayDataSorter
    dataProcessor = new InPlayDataProcessor(builder)
  }

  def cleanup() {
    dataProcessor = null
  }

  def "Test Data Decoupled"() {
    given:
    InPlayData data = TestTools.inPlayDataFromFile('InPlayDataProcessorTest/inPlayFull.json')
    consumer.consume() >> data
    InPlayData structureCaptor
    List<SportSegment> sportsCaptor
    SportsRibbon ribbonCaptor
    1 * storageService.save(_, _, _) >> { arguments ->
      structureCaptor = arguments[0]
      sportsCaptor = arguments[1]
      ribbonCaptor = arguments[2]
      structureCaptor instanceof InPlayData
      sportsCaptor instanceof List<SportSegment>
      ribbonCaptor instanceof SportsRibbon
      return 5L
    }
    SportsRibbon expectedSportsRibbon = data.getSportsRibbon()
    storageService.getLatestSportSegmentsObjects() >> new ArrayList<SportSegment>()
    when:
    dataProcessor.tryProcess()
    then:
    int sportSegmentsCount = data.getLivenow().getSportEvents().size() + data.getUpcoming().getSportEvents().size() + data.getLiveStream().getSportEvents().size()
    // all sport segments passed to storage + 2 for football Match betting market selector (1 for livenow and one for liveStream)
    sportSegmentsCount + 6 == sportsCaptor.size()
    // sport ribbon passed to storage
    expectedSportsRibbon == ribbonCaptor
    InPlayData structure = structureCaptor
    // type segments was removed in structure
    structure.getLivenow().getSportEvents().each { sport ->
      assert sport.getEventsByTypeName().isEmpty()
    }
    structure.getUpcoming().getSportEvents().each { sport ->
      assert sport.getEventsByTypeName().isEmpty()
    }
    structure.getLiveStream().getSportEvents().each { sport ->
      assert sport.getEventsByTypeName().isEmpty()
    }
    // ribbon was removed in storage
    structure.getSportsRibbon() == null
    1 * storageService.clearError()
  }
  def "Notifications were sent"() {
    given:
    InPlayData data = TestTools.inPlayDataFromFile('InPlayDataProcessorTest/inPlayFull.json')
    consumer.consume() >> data
    storageService.getLatestSportSegmentsObjects() >> new ArrayList<SportSegment>()
    storageService.save(_, _, _) >> 5L
    when:
    dataProcessor.tryProcess()
    then:
    1 * messagePublisher.publish(TopicType.IN_PLAY_STRUCTURE_CHANGED, '5')
    1 * messagePublisher.publish(TopicType.IN_PLAY_SPORTS_RIBBON_CHANGED, '5')
    1 * storageService.clearError()
  }
  def "Notifications were sent in pessimistic mode"() {
    given:
    InPlayData data = TestTools.inPlayDataFromFile('InPlayDataProcessorTest/inPlayFull.json')
    consumer.consume() >> data
    storageService.getLatestSportSegmentsObjects() >> new ArrayList<SportSegment>()
    storageService.getLatestInPlayDataObject() >> data
    storageService.save(_, _, _) >> 5L
    builder.isPessimisticModeEnabled() >> true
    dataProcessor = new InPlayDataProcessor(builder)
    when:
    dataProcessor.tryProcess()
    then:
    1 * messagePublisher.publish(TopicType.IN_PLAY_STRUCTURE_CHANGED, '5')
    1 * messagePublisher.publish(TopicType.IN_PLAY_SPORTS_RIBBON_CHANGED, '5')
    1 * storageService.clearError()
  }
  def "Notifications were not sent"() {
    given:
    //prepare captors
    InPlayData structureCaptor
    List<SportSegment> sportsCaptor
    SportsRibbon ribbonCaptor
    InPlayData data = TestTools.inPlayDataFromFile('InPlayDataProcessorTest/inPlayFull.json')
    when:
    dataProcessor.tryProcess()
    then:
    (1.._) * messagePublisher.publish(_, _)
    consumer.consume() >> data
    storageService.getLatestSportSegmentsObjects() >> data
    storageService.save(_, _, _) >> { arguments ->
      structureCaptor = arguments[0]
      sportsCaptor = arguments[1]
      ribbonCaptor = arguments[2]
      structureCaptor instanceof InPlayData
      sportsCaptor instanceof List<SportSegment>
      ribbonCaptor instanceof SportsRibbon
      return 5L
    }
    when:
    dataProcessor.tryProcess()
    then:
    consumer.consume() >> data
    storageService.getLatestInPlayDataObject() >> structureCaptor
    storageService.getLatestSportSegmentsObjects() >> sportsCaptor
    storageService.getLatestSportsRibbonObject() >> ribbonCaptor
    // simulate storage
    storageService.save(_, _, _) >> 5L
  }

  def "Change Detector comparison "() {
    given:
    InPlayData data = TestTools.inPlayDataFromFile('InPlayDataProcessorTest/inPlayFull.json')
    consumer.consume() >> data
    storageService.getLatestSportSegmentsObjects() >> data
    storageService.getLatestInPlayDataObject() >> data
    storageService.save(_, _, _) >> 5L
    when:
    dataProcessor.tryProcess()
    then:
    1 * messagePublisher.publish(TopicType.IN_PLAY_STRUCTURE_CHANGED, '5')
    1 * messagePublisher.publish(TopicType.IN_PLAY_SPORTS_RIBBON_CHANGED, '5')
    1 * storageService.clearError()
  }

  def "Change Detector isPessimisticModeEnabled true "() {
    given:
    InPlayData data = TestTools.inPlayDataFromFile('InPlayDataProcessorTest/inPlayFull.json')
    consumer.consume() >> data
    storageService.getLatestSportSegmentsObjects() >> new ArrayList<SportSegment>()
    storageService.getLatestInPlayDataObject() >> data
    storageService.save(_, _, _) >> 5L
    builder.isPessimisticModeEnabled() >> true
    dataProcessor = new InPlayDataProcessor(builder)

    when:
    dataProcessor.tryProcess()
    then:
    1 * messagePublisher.publish(TopicType.IN_PLAY_STRUCTURE_CHANGED, '5')
    1 * messagePublisher.publish(TopicType.IN_PLAY_SPORTS_RIBBON_CHANGED, '5')
    1 * storageService.clearError()
  }

  def "Change Detector false "() {
    given:
    InPlayData data = TestTools.inPlayDataFromFile('InPlayDataProcessorTest/inPlayFull.json')
    InPlayData inplayData = TestTools.inPlayDataFromFile('InPlayDataProcessorTest/inPlayData.json')
    consumer.consume() >> inplayData
    storageService.getLatestSportSegmentsObjects() >> new ArrayList<SportSegment>()
    storageService.getLatestInPlayDataObject() >> data
    storageService.save(_, _, _) >> 5L
    builder.isPessimisticModeEnabled() >> true
    dataProcessor = new InPlayDataProcessor(builder)


    when:
    dataProcessor.tryProcess()
    then:
    1 * messagePublisher.publish(TopicType.IN_PLAY_STRUCTURE_CHANGED, '5')
    1 * messagePublisher.publish(TopicType.IN_PLAY_SPORTS_RIBBON_CHANGED, '5')
    1 * storageService.clearError()
  }

  def "Change Detector comparison false "() {
    given:
    InPlayData data = TestTools.inPlayDataFromFile('InPlayDataProcessorTest/inPlayFull.json')
    InPlayData inplayData = TestTools.inPlayDataFromFile('InPlayDataProcessorTest/inPlayData.json')
    consumer.consume() >> inplayData
    storageService.getLatestSportSegmentsObjects() >> data
    storageService.getLatestInPlayDataObject() >> data
    storageService.save(_, _, _) >> 5L
    when:
    dataProcessor.tryProcess()
    then:
    1 * messagePublisher.publish(TopicType.IN_PLAY_STRUCTURE_CHANGED, '5')
    1 * messagePublisher.publish(TopicType.IN_PLAY_SPORTS_RIBBON_CHANGED, '5')
    1 * storageService.clearError()
  }



}
