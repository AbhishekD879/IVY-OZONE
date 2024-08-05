package com.coral.oxygen.edp.tracking.firstmarkets

import com.coral.oxygen.edp.configuration.MappingConfiguration
import com.coral.oxygen.edp.model.mapping.EventMapper
import com.coral.oxygen.edp.model.mapping.config.SportsConfig
import com.coral.oxygen.edp.model.mapping.converter.OrdinalToNumberConverter
import com.coral.oxygen.edp.model.output.OutputEvent
import com.coral.oxygen.edp.service.DfApiService
import com.coral.oxygen.edp.tracking.model.HorseDTO
import com.coral.oxygen.edp.tracking.model.RaceDTO
import com.egalacoral.spark.siteserver.api.BinaryOperation
import com.egalacoral.spark.siteserver.api.SimpleFilter
import com.egalacoral.spark.siteserver.api.SiteServerApi
import com.egalacoral.spark.siteserver.api.SiteServerException
import com.egalacoral.spark.siteserver.model.Children
import com.fasterxml.jackson.databind.ObjectMapper
import org.checkerframework.checker.nullness.Opt
import org.mockito.Mock
import org.springframework.core.io.ClassPathResource
import spock.lang.Specification
import org.assertj.core.api.Assertions
import org.junit.Assert
import static com.coral.oxygen.edp.TestUtil.deserializeListWithJackson
import static com.coral.oxygen.edp.TestUtil.deserializeWithJackson

class FirstMarketsDataConsumerSpec extends Specification {

  Long MOCK_EVENT_ID = 13622846L
  def CATEGORYID = 21;
  private SiteServerApi siteServerApi
  private EventMapper eventMapper
  private DfApiService dfApiService

  OutputEvent expectedEvent = deserializeWithJackson("/firstmarkets/event_firstmarkets_mapped.json", OutputEvent.class)
  Map<Long, RaceDTO> races = raceObjectMockData();

  private FirstmarketsDataConsumer consumer

  def setup() {

    ObjectMapper objectMapper = new ObjectMapper()
    eventMapper = new MappingConfiguration().eventMapper(
        new SportsConfig(new ClassPathResource("/sportsConfig.json"), objectMapper),
        new OrdinalToNumberConverter(new ClassPathResource("/ordinalToNumber.json"), objectMapper),
        Arrays.asList("285", "286", "288", "289", "290"))

    siteServerApi = Stub(SiteServerApi)
    dfApiService = Stub(DfApiService)
    consumer = new FirstmarketsDataConsumer(siteServerApi, 5, 3, eventMapper, dfApiService)
  }

  def "test consume for valid event id"() {
    given: 'Prepare event id Set'
    SimpleFilter simpleFilter = new SimpleFilter.SimpleFilterBuilder()
        .addBinaryOperation("event.siteChannels", BinaryOperation.contains, "M")
        .addBinaryOperation("market.siteChannels", BinaryOperation.contains, "M")
        .addField("market.isMarketBetInRun")
        .addField("market.isDisplayed")
        .build()
    List<Children> mockEvent = deserializeListWithJackson("/firstmarkets/event_firstmarkets_children.json", Children.class)

    siteServerApi.getEventToOutcomeForEvent(
        Collections.singletonList(String.valueOf(MOCK_EVENT_ID)),
        simpleFilter, null, Collections.emptyList()) >> Optional.of(mockEvent)

    dfApiService.getNextRaces(CATEGORYID, Set.of(MOCK_EVENT_ID)) >> Optional.of(races)
    when: 'Call consumers #doConsume()'
    def result = consumer.doConsume(Set.of(MOCK_EVENT_ID))
    then: 'Consumer returns the map with id as a key, and Event as a value'
    Assert.assertNotNull(result.get(MOCK_EVENT_ID))
    OutputEvent actualEvent = result.get(MOCK_EVENT_ID).getEvent()
    actualEvent.getName() == expectedEvent.getName()
    actualEvent.getMarkets().size() == expectedEvent.getMarkets().size()
    actualEvent.getComments() == expectedEvent.getComments()
  }

  def "test consume for valid event empty races data"() {
    given: 'Prepare event id Set'
    SimpleFilter simpleFilter = new SimpleFilter.SimpleFilterBuilder()
        .addBinaryOperation("event.siteChannels", BinaryOperation.contains, "M")
        .addBinaryOperation("market.siteChannels", BinaryOperation.contains, "M")
        .addField("market.isMarketBetInRun")
        .addField("market.isDisplayed")
        .build()
    List<Children> mockEvent = deserializeListWithJackson("/firstmarkets/event_firstmarkets_children.json", Children.class)

    siteServerApi.getEventToOutcomeForEvent(
        Collections.singletonList(String.valueOf(MOCK_EVENT_ID)),
        simpleFilter, null, Collections.emptyList()) >> Optional.of(mockEvent)
    Map<Long, RaceDTO> races = new HashMap<>()
    dfApiService.getNextRaces(CATEGORYID, Set.of(MOCK_EVENT_ID)) >> Optional.empty()

    when: 'Call consumers #doConsume()'
    def result = consumer.doConsume(Set.of(MOCK_EVENT_ID))
    then: 'Consumer returns the map with id as a key, and Event as a value'
    Assert.assertNotNull(result.get(MOCK_EVENT_ID))
    OutputEvent actualEvent = result.get(MOCK_EVENT_ID).getEvent()
    actualEvent.getName() == expectedEvent.getName()
    actualEvent.getMarkets().size() == expectedEvent.getMarkets().size()
    actualEvent.getComments() == expectedEvent.getComments()
  }

  def "test consume for valid event empty horses data"() {
    given: 'Prepare event id Set'
    SimpleFilter simpleFilter = new SimpleFilter.SimpleFilterBuilder()
        .addBinaryOperation("event.siteChannels", BinaryOperation.contains, "M")
        .addBinaryOperation("market.siteChannels", BinaryOperation.contains, "M")
        .addField("market.isMarketBetInRun")
        .addField("market.isDisplayed")
        .build()
    List<Children> mockEvent = deserializeListWithJackson("/firstmarkets/event_firstmarkets_children.json", Children.class)

    siteServerApi.getEventToOutcomeForEvent(
        Collections.singletonList(String.valueOf(MOCK_EVENT_ID)),
        simpleFilter, null, Collections.emptyList()) >> Optional.of(mockEvent)

    Map<Long, RaceDTO> races = horsesObjectMockData();

    dfApiService.getNextRaces(CATEGORYID, Set.of(MOCK_EVENT_ID)) >> Optional.of(races)

    when: 'Call consumers #doConsume()'
    def result = consumer.doConsume(Set.of(MOCK_EVENT_ID))
    then: 'Consumer returns the map with id as a key, and Event as a value'
    Assert.assertNotNull(result.get(MOCK_EVENT_ID))
    OutputEvent actualEvent = result.get(MOCK_EVENT_ID).getEvent()
    actualEvent.getName() == expectedEvent.getName()
    actualEvent.getMarkets().size() == expectedEvent.getMarkets().size()
    actualEvent.getComments() == expectedEvent.getComments()
  }

  Map<Long, RaceDTO> horsesObjectMockData(){
    Map<Long, RaceDTO> races = new HashMap<Long,RaceDTO>()
    RaceDTO raceDTO = new RaceDTO()
    List<HorseDTO> horseDtoList = new ArrayList<HorseDTO>()
    HorseDTO dto = new HorseDTO()
    dto.setDraw("1")
    dto.setSilk("123.png")
    dto.setJockey("Daniel")
    dto.setHorseAge(20)
    horseDtoList.add(dto)
    horseDtoList.add(null)
    raceDTO.setHorses(horseDtoList)
    races.put(13622846L,raceDTO)
    races
  }

  Map<Long, RaceDTO> raceObjectMockData(){
    Map<Long, RaceDTO> races = new HashMap<Long,RaceDTO>()
    RaceDTO raceDTO = new RaceDTO()
    List<HorseDTO> horseDtoList = new ArrayList<HorseDTO>()
    HorseDTO dto = new HorseDTO()
    dto.setDraw("1")
    dto.setSilk("123.png")
    dto.setJockey("Daniel")
    dto.setHorseAge(20)
    HorseDTO dto1 = new HorseDTO()
    dto1.setDraw("3")
    dto1.setSilk("567.png")
    dto1.setJockey("stake")
    dto1.setHorseAge(12)
    horseDtoList.add(dto)
    horseDtoList.add(dto1)

    raceDTO.setHorses(horseDtoList)
    races.put(13622846L,raceDTO)
    races
  }

  def "test consume for Invalid event id with siteserveexception"() {
    given: 'Prepare event id Set'
    //Optional<List<Children>> mockEvent = new ArrayList<List<Children>>()
    SimpleFilter simpleFilter = new SimpleFilter.SimpleFilterBuilder()
        .addBinaryOperation("event.siteChannels", BinaryOperation.contains, "M")
        .addBinaryOperation("market.siteChannels", BinaryOperation.contains, "M")
        .addField("market.isMarketBetInRun")
        .addField("market.isDisplayed")
        .build()

    siteServerApi.getEventToOutcomeForEvent(
        Collections.singletonList(String.valueOf(MOCK_EVENT_ID)),
        simpleFilter, null, Collections.emptyList()) >> Optional.empty()
    dfApiService.getNextRaces(CATEGORYID, Set.of(MOCK_EVENT_ID)) >> Optional.of(races)
    when: 'Call consumers #doConsume()'
    def result = consumer.doConsume(Set.of(MOCK_EVENT_ID))
    then: 'Consumer returns the map with id as a key, and Event as a value'
    final SiteServerException exception = thrown()
  }

  def "test consume for throw IOException for DF Call"() {
    given: 'Prepare event id Set'
    dfApiService.getNextRaces(CATEGORYID, Set.of(MOCK_EVENT_ID)) >> { throw new IOException("DF API Call")}
    when:
    def result = consumer.doConsume(Set.of(MOCK_EVENT_ID))
    then: 'Consumer returns the map with id as a key, and Event as a value'
    notThrown(IOException)
  }
}
