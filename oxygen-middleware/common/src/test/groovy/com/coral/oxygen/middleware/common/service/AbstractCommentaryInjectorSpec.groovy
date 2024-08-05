package com.coral.oxygen.middleware.common.service

import static com.coral.oxygen.middleware.common.service.AbstractCommentaryInjector.AWAY_ROLE_CODE
import static com.coral.oxygen.middleware.common.service.AbstractCommentaryInjector.HOME_ROLE_CODE

import com.coral.oxygen.cms.api.SystemConfigProvider
import com.coral.oxygen.middleware.common.service.commentary.AbstractModel
import com.coral.oxygen.middleware.common.service.commentary.CommentaryService
import com.coral.oxygen.middleware.common.service.commentary.Period
import com.coral.oxygen.middleware.common.service.commentary.TeamScore
import com.coral.oxygen.middleware.pojos.model.cms.CmsSystemConfig
import com.coral.oxygen.middleware.pojos.model.output.EventsModuleData
import com.egalacoral.spark.siteserver.model.Event
import com.fasterxml.jackson.core.type.TypeReference
import com.fasterxml.jackson.databind.DeserializationFeature
import com.fasterxml.jackson.databind.ObjectMapper
import com.google.gson.Gson
import com.google.gson.GsonBuilder
import com.oxygen.middleware.common.utils.TestUtils

import groovy.json.JsonSlurper

import java.nio.file.Files
import java.nio.file.Path
import java.nio.file.Paths
import java.util.function.Function
import java.util.stream.Collectors
import java.util.stream.LongStream

import spock.lang.Shared
import spock.lang.Specification

class AbstractCommentaryInjectorSpec extends Specification {

  AbstractSiteServeService siteServeService = Mock()
  SystemConfigProvider systemConfigProvider = Mock()
  CommentaryService commentaryService = Mock()
  JsonSlurper json = new JsonSlurper()

  @Shared
  CmsSystemConfig cmsSystemConfig

  @Shared
  Gson gson

  def setupSpec() {
    cmsSystemConfig = new CmsSystemConfig()
    cmsSystemConfig.bipScoreEvents = [
      '52': true,
      '36': true,
      '20': false
    ]

    gson = new GsonBuilder().create()
  }

  def "Test injected data"() {
    given:
    List<Long> eventsIds = LongStream.of(7000546, 6992907, 6992049, 6990925, 6963593).boxed().collect(Collectors.toList())
    def eventsJsonFile = getClass().getClassLoader().getResourceAsStream('InputModuleDataItems.json')
    def mapper = new ObjectMapper()
    mapper.disable(DeserializationFeature.FAIL_ON_UNKNOWN_PROPERTIES)
    List<EventsModuleData> inEvents = mapper.readValue(eventsJsonFile, new TypeReference<List<EventsModuleData>>() {
        })
    def commentaryStream = getClass().getClassLoader().getResourceAsStream('commentary.json')
    List<Event> lsEvents = mapper.readValue(commentaryStream, new TypeReference<List<Event>>() { })

    siteServeService.getCommentaryForEvent(Arrays.asList('7000546', '6992907', '6992049')) >> lsEvents.stream().collect(Collectors.toMap({ e -> e.getId() }, Function.identity()))
    systemConfigProvider.systemConfig() >> cmsSystemConfig

    AbstractCommentaryInjector spy = Spy(AbstractCommentaryInjector, constructorArgs: [
      siteServeService,
      systemConfigProvider
    ])

    when:
    spy.injectData(eventsIds, inEvents)

    then:
    3 * spy.populateEvent(_ as EventsModuleData, _ as Event)
  }

  def "PopulateBadmintonEvent"() {
    setup:
    def injectorInstance = new AbstractCommentaryInjector(siteServeService, systemConfigProvider)
    def event = TestUtils.parseFile('commentaryBadminton.json', Event.class)
    def moduleDataItem = new EventsModuleData()
    moduleDataItem.setCategoryCode('badminton')
    def expectedEvent = json.parseText(TestUtils.getResourse('responseBadminton.json'))

    when:
    injectorInstance.populateEvent(moduleDataItem, event)
    moduleDataItem.setUniqueId(null)

    then:
    def actualEvent = json.parseText(TestUtils.getGson(false).toJson(moduleDataItem))
    actualEvent == expectedEvent
  }

  def "PopulateTennisEvent"() {
    setup:
    def injectorInstance = new AbstractCommentaryInjector(siteServeService, systemConfigProvider)
    def event = TestUtils.parseFile('commentaryTennis.json', Event.class)
    def moduleDataItem = new EventsModuleData()
    moduleDataItem.setCategoryCode('tennis')
    def expectedEvent = json.parseText(TestUtils.getResourse('responseTennis.json'))

    when:
    injectorInstance.populateEvent(moduleDataItem, event)
    moduleDataItem.setUniqueId(null)

    then:
    def actualEvent = json.parseText(TestUtils.getGson(false).toJson(moduleDataItem))
    actualEvent == expectedEvent
  }

  def "Inject with PibScoreParser"() {
    setup:
    systemConfigProvider.systemConfig() >> cmsSystemConfig
    def eventJsonFile = getClass().getClassLoader().getResourceAsStream('VolleyballModuleDataItems.json')
    def mapper = new ObjectMapper()
    mapper.disable(DeserializationFeature.FAIL_ON_UNKNOWN_PROPERTIES)
    def parsedEvents = mapper.readValue(eventJsonFile, new TypeReference<List<EventsModuleData>>() { })

    AbstractCommentaryInjector spy = Spy(AbstractCommentaryInjector, constructorArgs: [
      siteServeService,
      systemConfigProvider
    ])
    spy.setCommentaryService(commentaryService)
    when:
    spy.injectWithBipScoreParser(parsedEvents)

    then:
    2 * spy.populateEventWithNameAndCommentary(_ as EventsModuleData)
  }

  def "Inject with PibScoreParser in not enabled in CMS"() {
    setup:
    def cmsSystemConfigWithFalse = new CmsSystemConfig()
    cmsSystemConfigWithFalse.bipScoreEvents = [
      '52': false,
      '36': false,
      '20': false,
    ]

    systemConfigProvider.systemConfig() >> cmsSystemConfigWithFalse
    def eventsJsonFile = getClass().getClassLoader().getResourceAsStream('VolleyballModuleDataItems.json')
    def mapper = new ObjectMapper()
    mapper.disable(DeserializationFeature.FAIL_ON_UNKNOWN_PROPERTIES)
    List<EventsModuleData> events = mapper.readValue(eventsJsonFile, new TypeReference<List<EventsModuleData>>() {
        })

    AbstractCommentaryInjector spy = Spy(AbstractCommentaryInjector, constructorArgs: [
      siteServeService,
      systemConfigProvider
    ])

    when:
    spy.injectWithBipScoreParser(events)

    then:
    0 * spy.populateEventWithNameAndCommentary(_ as EventsModuleData)
  }

  def "Test football locator"() {
    given:
    Event commentary4894821 = gson.fromJson(TestResources.Commentary4894821.getSource(), Event.class)
    EventsModuleData item = new EventsModuleData()
    AbstractCommentaryInjector spy = Spy(AbstractCommentaryInjector, constructorArgs: [
      siteServeService,
      systemConfigProvider
    ])

    when:
    spy.populateFootballComments(item, commentary4894821)
    def home = new TeamScore((Map<String, Object>) item.getComments().getTeams().get(HOME_ROLE_CODE))
    def away = new TeamScore((Map<String, Object>) item.getComments().getTeams().get(AWAY_ROLE_CODE))

    then:
    item.getComments().getTeams() != null
    item.getComments().getTeams().containsKey(HOME_ROLE_CODE)
    item.getComments().getTeams().containsKey(AWAY_ROLE_CODE)
    10 == item.getComments().getFacts().size()
    home.getScore() == '4'
    away.getScore() == '4'
    home.getPenaltyScore() == '1'
    away.getPenaltyScore() == '2'
    home.getExtraTimeScore() == '2'
    away.getExtraTimeScore() == '2'
  }

  def "Test football with team names are team1|2"() {
    Event commentary4894821 = gson.fromJson(TestResources.Commentary4894821_TEAM.getSource(), Event.class)
    EventsModuleData item = new EventsModuleData()
    AbstractCommentaryInjector spy = Spy(AbstractCommentaryInjector, constructorArgs: [
      siteServeService,
      systemConfigProvider
    ])

    when:
    spy.populateFootballComments(item, commentary4894821)
    def home = new TeamScore((Map<String, Object>) item.getComments().getTeams().get(HOME_ROLE_CODE))
    def away = new TeamScore((Map<String, Object>) item.getComments().getTeams().get(AWAY_ROLE_CODE))

    then:
    item.getComments().getTeams() != null
    item.getComments().getTeams().containsKey(HOME_ROLE_CODE)
    item.getComments().getTeams().containsKey(AWAY_ROLE_CODE)
    10 == item.getComments().getFacts().size()
    home.getScore() == '4'
    away.getScore() == '4'
    home.getPenaltyScore() == '1'
    away.getPenaltyScore() == '2'
    home.getExtraTimeScore() == '2'
    away.getExtraTimeScore() == '2'
  }

  def "Test extracting sub periods"() {
    given:
    Event commentary4894821 = gson.fromJson(TestResources.Commentary4894821.getSource(), Event.class)
    Period period = new Period(commentary4894821.getChildren().get(0).getEventPeriod())

    when:
    def subPeriods = period.extractSubPeriods()

    then:
    10 == period.getChildren().size()
    5 == subPeriods.size()
  }

  def "Test football no team"() {
    def commentary4894821 = gson.fromJson(TestResources.Commentary4894821_NoParticipants.getSource(), Event.class)
    def item = new EventsModuleData()
    AbstractCommentaryInjector spy = Spy(AbstractCommentaryInjector, constructorArgs: [
      siteServeService,
      systemConfigProvider
    ])

    when:
    spy.populateFootballComments(item, commentary4894821)

    then:
    item.getComments().getTeams() == null
  }

  def "Test population of comments"() {
    given:
    EventsModuleData item4894821 = gson.fromJson(TestResources.Event4894821.getSource(), EventsModuleData.class)
    Event commentary4894821 = gson.fromJson(TestResources.Commentary4894821.getSource(), Event.class)
    AbstractCommentaryInjector injector = Spy(AbstractCommentaryInjector, constructorArgs: [
      siteServeService,
      systemConfigProvider
    ])

    when:
    injector.populateComments(item4894821, commentary4894821)
    Map<String, Object> awayTeamScore = item4894821.getComments().getTeams().get('away')
    Map<String, Object> homeTeamScore = item4894821.getComments().getTeams().get('home')
    TeamScore awayExpected = new TeamScore(awayTeamScore)
    TeamScore homeExpected = new TeamScore(homeTeamScore)

    then:
    2 == item4894821.getComments().getTeams().size()
    awayExpected.equalByValues(getAway())
    homeExpected.equalByValues(getHome())
  }

  def "test Tenis event without commentaries"() {
    given:
    EventsModuleData event = gson.fromJson(TestResources.TennisEventWithoutCommentaries.getSource(), EventsModuleData.class)
    Event comments = gson.fromJson(TestResources.TennisEventWithoutCommentaries.getSource(), Event.class)
    AbstractCommentaryInjector injector = Spy(AbstractCommentaryInjector, constructorArgs: [
      siteServeService,
      systemConfigProvider
    ])
    when:
    injector.populateEvent(event, comments)
    then:
    noExceptionThrown()
  }

  def "Amelco commentary"() {
    given:
    Period amelcoRootEventPeriod = new Period(gson.fromJson(TestResources.AmelcoEventCommentaryEventPeriod.getSource(), Map.class))
    AbstractCommentaryInjector injector = Spy(AbstractCommentaryInjector, constructorArgs: [
      siteServeService,
      systemConfigProvider
    ])
    TeamScore home = new TeamScore(['id': 1406230])
    TeamScore away = new TeamScore(['id': 1406229])
    when:
    injector.calculateScoreFromEventPeriodChildren(home, away, amelcoRootEventPeriod)
    then:
    home.getScore() == '3'
    away.getScore() == '2'
  }

  // ------- helpers --------

  static AbstractModel getAway() {
    AbstractModel away = new TeamScore(new HashMap<>())
    away.setField(TeamScore.FieldNames.id, '61768')
    away.setField(TeamScore.FieldNames.eventId, '4894821')
    away.setField(TeamScore.FieldNames.name, 'Club Atletico Presidente Franco')
    away.setField(TeamScore.FieldNames.type, 'T')
    away.setField(TeamScore.FieldNames.roleCode, 'AWAY')
    away.setField(TeamScore.FieldNames.role, 'Away Team')
    away.setField(TeamScore.FieldNames.score, '2')
    return away
  }

  static AbstractModel getHome() {
    AbstractModel home = new TeamScore(new HashMap<>())
    home.setField(TeamScore.FieldNames.id, '61767')
    home.setField(TeamScore.FieldNames.eventId, '4894821')
    home.setField(TeamScore.FieldNames.name, 'Cerro Porteno')
    home.setField(TeamScore.FieldNames.type, 'T')
    home.setField(TeamScore.FieldNames.roleCode, 'HOME')
    home.setField(TeamScore.FieldNames.role, 'Home Team')
    home.setField(TeamScore.FieldNames.score, '2')
    return home
  }

  enum TestResources {

    Commentary4894821_TEAM('commentary/commentary4894821_TEAM.json'),
    Commentary4894821_NoParticipants('commentary/commentary4894821_NoParticipants.json'),
    Commentary4894821('commentary/commentary4894821.json'),
    Event4894821('commentary/event4894821.json'),
    TennisEventWithoutCommentaries('commentary/tennisNoPeriods.json'),
    AmelcoEventCommentaryEventPeriod('commentary/amelcoEventPeriod.json')

    private final String source

    TestResources(String fileName) {
      Path resource = Paths.get(ClassLoader.getSystemResource(fileName).toURI())
      this.source = new String(Files.readAllBytes(resource))
    }

    String getSource() {
      return source
    }

  }

}
