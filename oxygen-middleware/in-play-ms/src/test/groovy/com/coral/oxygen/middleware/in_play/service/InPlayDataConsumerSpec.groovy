package com.coral.oxygen.middleware.in_play.service

import com.coral.oxygen.cms.api.CmsService
import com.coral.oxygen.cms.api.SystemConfigProvider
import com.coral.oxygen.df.api.DFService
import com.coral.oxygen.middleware.common.configuration.MappersConfiguration
import com.coral.oxygen.middleware.common.mappers.EventMapper
import com.coral.oxygen.middleware.common.mappers.MarketMapper
import com.coral.oxygen.middleware.common.service.AssetManagementService
import com.coral.oxygen.middleware.common.service.MarketTemplateNameService
import com.coral.oxygen.middleware.common.service.SportsConfig
import com.coral.oxygen.middleware.common.utils.OrdinalToNumberConverter
import com.coral.oxygen.middleware.in_play.service.injector.*
import com.coral.oxygen.middleware.in_play.service.scoreboards.ScoreboardCache
import com.coral.oxygen.middleware.in_play.service.siteserver.InplaySiteServeService
import com.coral.oxygen.middleware.pojos.model.cms.CmsInplayData
import com.coral.oxygen.middleware.pojos.model.cms.CmsSystemConfig
import com.coral.oxygen.middleware.pojos.model.cms.VirtualSportDto
import com.coral.oxygen.middleware.pojos.model.df.Horse
import com.coral.oxygen.middleware.pojos.model.df.RaceEvent
import com.coral.oxygen.middleware.pojos.model.output.inplay.InPlayData
import com.egalacoral.spark.liveserver.utils.JsonMapper
import com.egalacoral.spark.siteserver.api.ExistsFilter
import com.egalacoral.spark.siteserver.api.LimitToFilter
import com.egalacoral.spark.siteserver.api.SimpleFilter
import com.egalacoral.spark.siteserver.api.SiteServerApi
import com.egalacoral.spark.siteserver.model.Aggregation
import com.egalacoral.spark.siteserver.model.Category
import com.egalacoral.spark.siteserver.model.Event
import org.mockito.Mockito
import org.springframework.cache.CacheManager
import org.springframework.core.io.ClassPathResource
import spock.lang.Ignore
import spock.lang.Specification

import java.util.function.Function
import java.util.stream.Collectors

class InPlayDataConsumerSpec extends Specification {

  CmsService cmsService = Mock()
  DFService dfService = Mock()
  SystemConfigProvider systemConfigProvider = Mock()
  InplaySiteServeService siteServeService = Mock()
  SiteServerApi siteServerApi = Mock()
  MarketTemplateNameService marketTemplateNameService = Mock()
  org.springframework.cache.Cache cache = Mock()
  InPlayStorageService storageService = Mock()
  ScoreboardCache scoreboardCache = Mock()
  JsonMapper jsonMapper = Mock();
  CmsSystemConfig cmsSystemConfig
  InPlayDataConsumer dataConsumer
  Event[] events1
  Event[] eventIdsEmpty
  Event[] virtualEvents
  CmsInplayData initialData
  Category[] virtualCategories
  CacheManager cacheManager = Mock()
  AssetManagementService assetManagementService = Mock()
  private static final String VIRTUAL_SPORTS = "virtualSports";
  private static final String VIRTUAL_SPORT_CACHE = "virtualSportsCache";

  InPlayData data
  InPlayData expectedData
  Map<Long, RaceEvent> races = raceObjectMockData();
  Map<Long, RaceEvent> races1 =  raceHRObjectMockData()

  def setup() {
    initialData = TestTools.initialDataFromFile("CMSDataInjectorTest/cmsData.json")
    cmsService.requestInplayData() >> initialData
    Category[] categories1 = TestTools.fromFile("InPlayDataConsumerTest/classes1.json", Category[].class)
    events1 = TestTools.fromFile("InPlayDataConsumerTest/events1.json", Event[].class)
    Map<String, Integer> marketCountForEvent = new HashMap<>();
    marketCountForEvent.put("5006498",1);
    marketCountForEvent.put("5022056",1);
    marketCountForEvent.put("5035188",1);
    marketCountForEvent.put("5190521",1);
    marketCountForEvent.put("5190252",1);
    marketCountForEvent.put("5190177",1);
    siteServeService.getClasses(Mockito.any()) >>  categories1
    siteServeService.getEvents(*_) >> events1
    siteServeService.getEventsForClassWithPrimaryMarkets(*_) >> events1
    siteServeService.getMarketsCountPerEventForClass(*_) >> marketCountForEvent
    siteServeService.getHRMarketsCountPerEventForClass(*_) >> marketCountForEvent

    eventIdsEmpty = TestTools.fromFile("InPlayDataConsumerTest/events3.json", Event[].class)
    virtualEvents = TestTools.fromFile("InPlayDataConsumerTest/virtualEvents.json",Event[].class)
    virtualCategories = TestTools.fromFile("InPlayDataConsumerTest/virtualCategories.json",Category[].class)
    Optional<ScoreboardCache> scoreboard = Optional.empty()
    siteServeService.getClassesforVirtualHub() >> virtualCategories
    cmsService.getVirtualSportsByBrand() >> initialData.getVirtualSports()
    siteServeService.getVirtualEvents(*_) >> virtualEvents
    scoreboardCache.findById(*_) >> scoreboard

    Aggregation[] aggregation1 = TestTools.fromFile("InPlayDataConsumerTest/marketsCount1.json", Aggregation[].class)
    Aggregation[] aggregation2 = TestTools.fromFile("InPlayDataConsumerTest/marketsCount3.json", Aggregation[].class)
    Aggregation[] aggregation3 = TestTools.fromFile("InPlayDataConsumerTest/marketsCount4.json", Aggregation[].class)

    Event[] comments = TestTools.fromFile("InPlayDataConsumerTest/comments.json", Event[].class)

    MappersConfiguration mappersConfiguration = new MappersConfiguration()
    SportsConfig sportsConfig = new SportsConfig(new ClassPathResource("sportsConfig.json"), TestTools.GSON)
    OrdinalToNumberConverter ordinalToNumberConverter = new OrdinalToNumberConverter(new ClassPathResource("ordinalToNumber.json"), TestTools.GSON)
    MarketMapper marketMapper = mappersConfiguration.marketMapper(siteServerApi, sportsConfig, ordinalToNumberConverter, marketTemplateNameService)
    EventMapper eventMapper = mappersConfiguration.eventInplayMapper(marketMapper)
    InplayCommentaryInjector commentaryInjector = new InplayCommentaryInjector(siteServeService, systemConfigProvider)
    InPlayDataFilter dataFilter = new InPlayDataFilter()
    SportsRibbonService ribbonService = new SportsRibbonService()
    InPlayDataSorter dataSorter = new InPlayDataSorter()
    InPlayEventIdsInjector idsInjector = new InPlayEventIdsInjector()
    CMSDataInjector cmsDataInjector = new CMSDataInjector()
    SportsConfigDataInjector sportsConfigDataInjector = new SportsConfigDataInjector(sportsConfig)
    TypeSectionTitleDataInjector sectionTitleDataInjector = new TypeSectionTitleDataInjector()
    InPlayEventCountInjector inPlayEventCountInjector = new InPlayEventCountInjector()
    ScoreBoardStatsInjector scoreBoardStatsInjector = new ScoreBoardStatsInjector(List.of(16),scoreboardCache,jsonMapper);

    InPlayDataInjectorFactory dataInjectorFactory = new InPlayDataInjectorFactory(
        inPlayEventCountInjector,
        idsInjector,
        sportsConfigDataInjector,
        commentaryInjector,
        sectionTitleDataInjector,
        cmsDataInjector,
        scoreBoardStatsInjector
        )
    dataConsumer = new InPlayDataConsumer(
        cmsService,
        eventMapper,
        marketMapper,
        dataFilter,
        ribbonService,
        dataSorter,
        marketTemplateNameService,
        dataInjectorFactory,
        siteServeService, dfService,cacheManager,assetManagementService)

    siteServerApi.getEventToOutcomeForClass(Arrays.asList("75", "97", "108", "166", "97", "108", "105"),
        _ as SimpleFilter,
        _ as LimitToFilter,
        _ as ExistsFilter) >>
        Optional.of(Arrays.asList(events1))

    siteServerApi.getEventMarketsCountForClass(Arrays.asList("75", "97", "108", "166"), _) >>
        Optional.of(Arrays.asList(aggregation1))

    siteServerApi.getEventMarketsCountForClass(Arrays.asList("97", "108", "105"), _) >>
        Optional.of(Arrays.asList(aggregation1))

    siteServerApi.getEventMarketsCountForClass(Arrays.asList("16322"), _) >>
        Optional.of(Arrays.asList(aggregation2))

    siteServerApi.getEventMarketsCountForClass(Arrays.asList("195"), _) >>
        Optional.of(Arrays.asList(aggregation3))

    siteServerApi.getEventMarketsCountForClass(Arrays.asList("266"), _) >>
        Optional.of(Arrays.asList(aggregation3))

    siteServeService.getCommentaryForEvent(*_) >>
        Arrays.asList(comments).stream().collect(Collectors.toMap({ e -> e.getId()}, Function.identity()))

    cmsSystemConfig = new CmsSystemConfig()
    cmsSystemConfig.bipScoreEvents = [
      '52': true,
      '36': true,
      '20': true
    ]
    systemConfigProvider.systemConfig() >> cmsSystemConfig
  }

  def cleanup() {
    dataConsumer = null
  }

  @Ignore
  def "DataConsumer test with PR Markets"() {
    marketTemplateNameService.containsName(*_) >> {type, templateName -> return templateName != null && type.toString().replaceAll("_", "").equalsIgnoreCase(templateName.replaceAll("\\s", ""))}
    Category[] categories1 = TestTools.fromFile("InPlayDataConsumerTest/classes1.json", Category[].class)
    siteServeService.getClasses(*_) >>  categories1
    siteServeService.getEvents(*_) >> events1
    siteServeService.getEventsForClassWithPrimaryMarkets(*_) >> events1
    dfService.getRaceEvents(*_) >> races

    data = dataConsumer.consume()
    expectedData = TestTools.inPlayDataFromFile("InPlayDataConsumerTest/resultWithPRMarket.json")
    expectedData.setCreationTime(data.creationTime())

    expect:
    data.getLivenow().eventCount >= 0
  }

  @Ignore
  def "DataConsumer test with PR Markets withoutDFResponse"() {
    marketTemplateNameService.containsName(*_) >> {type, templateName -> return templateName != null && type.toString().replaceAll("_", "").equalsIgnoreCase(templateName.replaceAll("\\s", ""))}
    Category[] categories1 = TestTools.fromFile("InPlayDataConsumerTest/classes1.json", Category[].class)
    siteServeService.getClasses(*_) >>  categories1
    siteServeService.getEvents(*_) >> events1
    siteServeService.getEventsForClassWithPrimaryMarkets(*_) >> events1
    dfService.getRaceEvents(*_) >> races1

    data = dataConsumer.consume()
    expectedData = TestTools.inPlayDataFromFile("InPlayDataConsumerTest/resultWithPRMarket.json")
    expectedData.setCreationTime(data.creationTime())

    expect:
    data.getLivenow().eventCount >= 0
  }

  def "DataConsumer test with PR Markets withoutDFResponseEmpty"() {
    marketTemplateNameService.containsName(*_) >> {type, templateName -> return templateName != null && type.toString().replaceAll("_", "").equalsIgnoreCase(templateName.replaceAll("\\s", ""))}
    Category[] categories1 = TestTools.fromFile("InPlayDataConsumerTest/classes1.json", Category[].class)
    siteServeService.getClasses(*_) >>  categories1
    siteServeService.getEvents(*_) >> events1
    siteServeService.getEventsForClassWithPrimaryMarkets(*_) >> events1
    cacheManager.getCache(VIRTUAL_SPORT_CACHE) >> cache
    dfService.getRaceEvents(*_) >> Optional.empty()
    data = dataConsumer.consume()
    expectedData = TestTools.inPlayDataFromFile("InPlayDataConsumerTest/resultWithPRMarket.json")
    expectedData.setCreationTime(data.creationTime())
    expect:
    data.getLivenow().eventCount >= 0
  }




  def "DataConsumer test with virtual sports Empty"() {
    initialData.setVirtualSports(null);
    marketTemplateNameService.containsName(*_) >> {type, templateName -> return templateName != null && type.toString().replaceAll("_", "").equalsIgnoreCase(templateName.replaceAll("\\s", ""))}
    Category[] categories1 = TestTools.fromFile("InPlayDataConsumerTest/classes1.json", Category[].class)
    siteServeService.getClasses(*_) >>  categories1
    siteServeService.getEvents(*_) >> events1
    List<VirtualSportDto> virtualSportDtoList = cmsService.getVirtualSportsByBrand();
    //cmsService.getVirtualSportsByBrand() >>  virtualSportDtoList
    siteServeService.getEventsForClassWithPrimaryMarkets(*_) >> events1
    List<Event> list = new ArrayList<>();
    cacheManager.getCache(VIRTUAL_SPORT_CACHE) >> cache
    cache.get(VIRTUAL_SPORTS,List.class) >> list;
    dfService.getRaceEvents(*_) >> Optional.empty()
    data = dataConsumer.consume()
    expectedData = TestTools.inPlayDataFromFile("InPlayDataConsumerTest/resultWithPRMarket.json")
    expectedData.setCreationTime(data.creationTime())
    expect:
    data.getLivenow().eventCount >= 0
  }


  def "DataConsumer test with PR Markets with virtual events not Empty"() {
    marketTemplateNameService.containsName(*_) >> {type, templateName -> return templateName != null && type.toString().replaceAll("_", "").equalsIgnoreCase(templateName.replaceAll("\\s", ""))}
    Category[] categories1 = TestTools.fromFile("InPlayDataConsumerTest/classes1.json", Category[].class)
    siteServeService.getClasses(*_) >>  categories1
    siteServeService.getEvents(*_) >> events1
    siteServeService.getEventsForClassWithPrimaryMarkets(*_) >> events1
    List<Event> list = new ArrayList<>();
    cacheManager.getCache(VIRTUAL_SPORT_CACHE) >> cache
    cache.get(VIRTUAL_SPORTS,List.class) >> list;
    dfService.getRaceEvents(*_) >> Optional.empty()
    data = dataConsumer.consume()
    expectedData = TestTools.inPlayDataFromFile("InPlayDataConsumerTest/resultWithPRMarket.json")
    expectedData.setCreationTime(data.creationTime())
    expect:
    data.getLivenow().eventCount >= 0
  }


  def "DataConsumer test with PR Markets with cache Empty"() {
    marketTemplateNameService.containsName(*_) >> {type, templateName -> return templateName != null && type.toString().replaceAll("_", "").equalsIgnoreCase(templateName.replaceAll("\\s", ""))}
    Category[] categories1 = TestTools.fromFile("InPlayDataConsumerTest/classes1.json", Category[].class)
    siteServeService.getClasses(*_) >>  categories1
    siteServeService.getEvents(*_) >> events1
    siteServeService.getEventsForClassWithPrimaryMarkets(*_) >> events1
    cacheManager.getCache(VIRTUAL_SPORT_CACHE) >> null
    dfService.getRaceEvents(*_) >> Optional.empty()
    data = dataConsumer.consume()
    expectedData = TestTools.inPlayDataFromFile("InPlayDataConsumerTest/resultWithPRMarket.json")
    expectedData.setCreationTime(data.creationTime())
    expect:
    data.getLivenow().eventCount >= 0
  }

  def "DataConsumer test with PR Markets eventIdsEmpty"() {
    marketTemplateNameService.containsName(*_) >> {type, templateName -> return templateName != null && type.toString().replaceAll("_", "").equalsIgnoreCase(templateName.replaceAll("\\s", ""))}
    Category[] categories2 = TestTools.fromFile("InPlayDataConsumerTest/classes2.json", Category[].class)
    siteServeService.getClasses(*_) >>  categories2
    siteServeService.getEvents(*_) >> eventIdsEmpty
    siteServeService.getEventsForClassWithPrimaryMarkets(*_) >> eventIdsEmpty
    dfService.getRaceEvents(*_) >> Optional.empty()
    cacheManager.getCache(VIRTUAL_SPORT_CACHE) >> cache
    data = dataConsumer.consume()
    expectedData = TestTools.inPlayDataFromFile("InPlayDataConsumerTest/resultWithPRMarket.json")
    expectedData.setCreationTime(data.creationTime())
    expect:
    data.getLivenow().eventCount >= 0
  }
  def "consume CmsInplayData Null"() {
    given:
    def  CmsInplayData cmsInplayData=new CmsInplayData();
    cmsInplayData.setActiveSportCategories(new ArrayList<>())
    storageService.getLatestCmsInPlayCache() >> cmsInplayData
    when:
    data = dataConsumer.consume()
    then:
    thrown(NullPointerException)
  }

  Map<Long, RaceEvent> raceFormEventEmptyMockData(){
    Map<Long, RaceEvent> races = new HashMap<Long,RaceEvent>()
    RaceEvent raceEvent = new RaceEvent()
    List<Horse> horseDtoList = new ArrayList<Horse>()
    horseDtoList.add(null)
    races.put(5006498L,raceEvent)
    races
  }

  Map<Long, RaceEvent> raceHRObjectMockData(){
    Map<Long, RaceEvent> races = new HashMap<Long,RaceEvent>()
    RaceEvent raceEvent = new RaceEvent()
    List<Horse> horseDtoList = new ArrayList<Horse>()
    Horse dto = new Horse()
    dto.setDraw("1")
    dto.setSilk("123.png")
    dto.setJockey("Daniel")
    dto.setHorseAge(20)
    raceEvent.setDistance(null)
    raceEvent.setRaceClass(null)
    raceEvent.setGoing(null)
    horseDtoList.add(dto)
    horseDtoList.add(null)
    raceEvent.setHorses(horseDtoList)
    races.put(5006498L,raceEvent)
    races
  }

  Map<Long, RaceEvent> raceObjectMockData(){
    Map<Long, RaceEvent> races = new HashMap<Long,RaceEvent>()
    RaceEvent raceDTO = new RaceEvent()
    List<Horse> horseDtoList = new ArrayList<Horse>()
    Horse dto = new Horse()
    dto.setDraw("1")
    dto.setSilk("123.png")
    dto.setJockey("Daniel")
    dto.setHorseAge(20)
    Horse dto1 = new Horse()
    dto1.setDraw("3")
    dto1.setSilk("567.png")
    dto1.setJockey("stake")
    dto1.setHorseAge(12)
    horseDtoList.add(dto)
    horseDtoList.add(dto1)
    raceDTO.setDistance("1m 2f")
    raceDTO.setRaceClass(7)
    raceDTO.setGoing("Good")
    raceDTO.setHorses(horseDtoList)
    races.put(5006498L,raceDTO)
    races
  }
}
