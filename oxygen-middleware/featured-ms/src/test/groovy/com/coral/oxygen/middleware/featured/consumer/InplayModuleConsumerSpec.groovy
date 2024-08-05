package com.coral.oxygen.middleware.featured.consumer

import com.coral.oxygen.middleware.featured.consumer.sportpage.InplayModuleConsumer
import com.coral.oxygen.middleware.featured.consumer.sportpage.ModuleConsumer
import com.coral.oxygen.middleware.featured.service.InplayDataService
import com.coral.oxygen.middleware.featured.service.injector.EventDataInjector
import com.coral.oxygen.middleware.featured.service.injector.FeaturedCommentaryInjector
import com.coral.oxygen.middleware.featured.utils.TestUtils
import com.coral.oxygen.middleware.pojos.model.cms.featured.InPlayConfig
import com.coral.oxygen.middleware.pojos.model.cms.featured.SportModule
import com.coral.oxygen.middleware.pojos.model.cms.featured.SportPageModule
import com.coral.oxygen.middleware.pojos.model.output.EventsModuleData
import com.coral.oxygen.middleware.pojos.model.output.featured.InplayModule
import com.coral.oxygen.middleware.pojos.model.output.featured.SegmentView
import com.coral.oxygen.middleware.pojos.model.output.inplay.InPlayData
import com.coral.oxygen.middleware.pojos.model.output.inplay.SportSegment
import com.coral.oxygen.middleware.pojos.model.output.inplay.TypeSegment
import spock.lang.Specification

import java.util.stream.Collectors

class InplayModuleConsumerSpec extends Specification {

  InplayDataService inplayDataService
  FeaturedCommentaryInjector featuredCommentaryInjector
  EventDataInjector eventDataInjector

  ModuleConsumer inplayModuleConsumer

  void setup() {
    inplayDataService = Mock(InplayDataService.class)
    featuredCommentaryInjector = Mock(FeaturedCommentaryInjector.class)
    eventDataInjector = Mock(EventDataInjector.class)
    inplayModuleConsumer = new InplayModuleConsumer(inplayDataService, eventDataInjector, featuredCommentaryInjector)
  }

  def "build inplay module for home page"() throws Exception {

    given: "cms inplay module configuaration"
    InPlayConfig cmsModuleConfig = TestUtils.deserializeWithGson("inplayModuleConsumer/homePage/cmsConfig.json",
        InPlayConfig.class)

    SportModule sportModule = new SportModule()
    sportModule.setSportId(0)
    sportModule.setId("aaa-bbb-ccc")

    SportPageModule sportPageModule = new SportPageModule(sportModule, Arrays.asList(cmsModuleConfig))

    and: "inplay data generation is 484"
    inplayDataService.getInplayDataVersion() >> "484"

    and: "inplay data is"
    inplayDataService.getInplayData("484") >> TestUtils.deserializeWithGson("inplayModuleConsumer/homePage/inplayData.json",
        InPlayData.class)

    and: "first sport segment in InplayData is Football"
    inplayDataService.getSportSegment("484", 16) >> TestUtils.deserializeWithGson("inplayModuleConsumer/homePage/sportSegment1.json",
        SportSegment.class)

    and: "second sport segment in InplayData is Tennis"
    inplayDataService.getSportSegment("484", 34) >> TestUtils.deserializeWithGson("inplayModuleConsumer/homePage/sportSegment2.json",
        SportSegment.class)

    when:
    InplayModule inplayModule = (InplayModule) inplayModuleConsumer.processModule(sportPageModule, null ,Collections.EMPTY_SET)


    then: "inplay module contains total number of all live now events"
    inplayModule.totalEvents == 105

    and: "sport segment 1 has 2 events"
    2 == inplayModule.getData().get(0).getEventCount()

    and: "sport segment 2 has 3 events"
    3 == inplayModule.getData().get(1).getEventCount()

    and: "events are updated only for one football type"
    1*eventDataInjector.injectData(_, _)

    and: "events commentary is triggered both fo football types & tennis types"
    5*featuredCommentaryInjector.injectData(_, _)
  }

  def "build segmented inplay module for home page"() throws Exception {

    given: "cms inplay module configuaration"
    InPlayConfig cmsModuleConfig = TestUtils.deserializeWithGson("inplayModuleConsumer/homePage/cmsConfigWithSegments.json",
        InPlayConfig.class)

    SportModule sportModule = new SportModule()
    sportModule.setSportId(0)
    sportModule.setId("aaa-bbb-ccc")
    sportModule.setSortOrder(2)

    SportPageModule sportPageModule = new SportPageModule(sportModule, Arrays.asList(cmsModuleConfig))

    and: "inplay data generation is 484"
    inplayDataService.getInplayDataVersion() >> "484"

    and: "inplay data is"
    inplayDataService.getInplayData("484") >> TestUtils.deserializeWithGson("inplayModuleConsumer/homePage/inplayData.json",
        InPlayData.class)

    and: "first sport segment in InplayData is Football"
    inplayDataService.getSportSegment("484", 16) >> TestUtils.deserializeWithGson("inplayModuleConsumer/homePage/sportSegment1.json",
        SportSegment.class)

    and: "second sport segment in InplayData is Tennis"
    inplayDataService.getSportSegment("484", 34) >> TestUtils.deserializeWithGson("inplayModuleConsumer/homePage/sportSegment2.json",
        SportSegment.class)


    InplayModule inplayModule = (InplayModule) inplayModuleConsumer.processModule(sportPageModule, null ,Collections.EMPTY_SET)
    Map<String, SegmentView> segmentWiseModules = new HashMap<>();
    when:
    inplayModuleConsumer.processSegmentwiseModules(
        inplayModule, segmentWiseModules, "InplayModule")

    then: "inplay module contains total number of segmentWiseModules"
    segmentWiseModules.size() == 3
  }

  def "build segmented inplay module with categorycode empty for home page"() throws Exception {

    given: "cms inplay module configuaration"
    InPlayConfig cmsModuleConfig = TestUtils.deserializeWithGson("inplayModuleConsumer/homePage/cmsConfigWithSegments.json",
        InPlayConfig.class)
    cmsModuleConfig.getHomeInplaySports().get(0).getSegmentReferences().get(0).setDisplayOrder(-1)
    SportModule sportModule = new SportModule()
    sportModule.setSportId(0)
    sportModule.setId("aaa-bbb-ccc")
    sportModule.setSortOrder(2)

    SportPageModule sportPageModule = new SportPageModule(sportModule, Arrays.asList(cmsModuleConfig))

    and: "inplay data generation is 484"
    inplayDataService.getInplayDataVersion() >> "484"

    and: "inplay data is"
    inplayDataService.getInplayData("484") >> TestUtils.deserializeWithGson("inplayModuleConsumer/homePage/inplayData.json",
        InPlayData.class)

    and: "first sport segment in InplayData is Football"
    inplayDataService.getSportSegment("484", 16) >> TestUtils.deserializeWithGson("inplayModuleConsumer/homePage/sportSegment1.json",
        SportSegment.class)

    and: "second sport segment in InplayData is Tennis"
    SportSegment sportSegment = TestUtils.deserializeWithGson("inplayModuleConsumer/homePage/sportSegment2.json",
        SportSegment.class)
    sportSegment.setCategoryCode("")
    inplayDataService.getSportSegment("484", 34) >> sportSegment


    InplayModule inplayModule = (InplayModule) inplayModuleConsumer.processModule(sportPageModule, null ,Collections.EMPTY_SET)
    Map<String, SegmentView> segmentWiseModules = new HashMap<>();
    when:
    inplayModuleConsumer.processSegmentwiseModules(
        inplayModule, segmentWiseModules, "InplayModule")

    then: "inplay module contains total number of segmentWiseModules"
    segmentWiseModules.size() == 2
  }
  def "build inplay module with categorycode empty for sport page"() throws Exception {

    given: "cms inplay module configuaration"
    InPlayConfig cmsModuleConfig = TestUtils.deserializeWithGson("inplayModuleConsumer/homePage/cmsConfigWithSegments.json",
        InPlayConfig.class)
    cmsModuleConfig.getHomeInplaySports().get(0).getSegmentReferences().get(0).setDisplayOrder(-1)
    SportModule sportModule = new SportModule()
    sportModule.setSportId(1)
    sportModule.setId("aaa-bbb-ccc")
    sportModule.setSortOrder(2)

    SportPageModule sportPageModule = new SportPageModule(sportModule, Arrays.asList(cmsModuleConfig))

    and: "inplay data generation is 484"
    inplayDataService.getInplayDataVersion() >> "484"

    and: "inplay data is"
    inplayDataService.getInplayData("484") >> TestUtils.deserializeWithGson("inplayModuleConsumer/homePage/inplayData.json",
        InPlayData.class)

    and: "first sport segment in InplayData is Football"
    inplayDataService.getSportSegment("484", 16) >> TestUtils.deserializeWithGson("inplayModuleConsumer/homePage/sportSegment1.json",
        SportSegment.class)

    and: "second sport segment in InplayData is Tennis"
    SportSegment sportSegment = TestUtils.deserializeWithGson("inplayModuleConsumer/homePage/sportSegment2.json",
        SportSegment.class)
    sportSegment.setCategoryCode("")
    inplayDataService.getSportSegment("484", 0) >> sportSegment


    InplayModule inplayModule = (InplayModule) inplayModuleConsumer.processModule(sportPageModule, null ,Collections.EMPTY_SET)
  }
  def "build segmented inplay module with no LiveNow for home page"() throws Exception {

    given: "cms inplay module configuaration"
    InPlayConfig cmsModuleConfig = TestUtils.deserializeWithGson("inplayModuleConsumer/homePage/cmsConfigWithSegments.json",
        InPlayConfig.class)
    cmsModuleConfig.getHomeInplaySports().get(0).getSegmentReferences().get(0).setDisplayOrder(-1)
    SportModule sportModule = new SportModule()
    sportModule.setSportId(0)
    sportModule.setId("aaa-bbb-ccc")
    sportModule.setSortOrder(2)

    SportPageModule sportPageModule = new SportPageModule(sportModule, Arrays.asList(cmsModuleConfig))

    and: "inplay data generation is 484"
    inplayDataService.getInplayDataVersion() >> "484"

    and: "inplay data is"
    InPlayData inPlayData = TestUtils.deserializeWithGson("inplayModuleConsumer/homePage/inplayData.json",
        InPlayData.class)
    inPlayData.getLivenow().getSportEvents().get(0).setCategoryId(null)
    inplayDataService.getInplayData("484") >> inPlayData

    and: "first sport segment in InplayData is Football"
    inplayDataService.getSportSegment("484", 16) >> TestUtils.deserializeWithGson("inplayModuleConsumer/homePage/sportSegment1.json",
        SportSegment.class)

    and: "second sport segment in InplayData is Tennis"
    SportSegment sportSegment = TestUtils.deserializeWithGson("inplayModuleConsumer/homePage/sportSegment2.json",
        SportSegment.class)
    inplayDataService.getSportSegment("484", 34) >> sportSegment


    InplayModule inplayModule = (InplayModule) inplayModuleConsumer.processModule(sportPageModule, null ,Collections.EMPTY_SET)
    Map<String, SegmentView> segmentWiseModules = new HashMap<>();
    when:
    inplayModuleConsumer.processSegmentwiseModules(
        inplayModule, segmentWiseModules, "InplayModule")

    then: "inplay module contains total number of segmentWiseModules"
    segmentWiseModules.size() == 0
  }

  def "limitEvents for inplay module for home page"() throws Exception {

    given: "cms inplay module configuaration"
    InPlayConfig cmsModuleConfig = TestUtils.deserializeWithGson("inplayModuleConsumer/homePage/cmsConfigWithSegments.json",
        InPlayConfig.class)
    cmsModuleConfig.setMaxEventCount(2)

    SportModule sportModule = new SportModule()
    sportModule.setSportId(0)
    sportModule.setId("aaa-bbb-ccc")
    sportModule.setSortOrder(2)

    SportPageModule sportPageModule = new SportPageModule(sportModule, Arrays.asList(cmsModuleConfig))

    and: "inplay data generation is 484"
    inplayDataService.getInplayDataVersion() >> "484"

    and: "inplay data is"
    inplayDataService.getInplayData("484") >> TestUtils.deserializeWithGson("inplayModuleConsumer/homePage/inplayData.json",
        InPlayData.class)

    and: "first sport segment in InplayData is Football"
    inplayDataService.getSportSegment("484", 16) >> TestUtils.deserializeWithGson("inplayModuleConsumer/homePage/sportSegment1.json",
        SportSegment.class)

    and: "second sport segment in InplayData is Tennis"
    inplayDataService.getSportSegment("484", 34) >> TestUtils.deserializeWithGson("inplayModuleConsumer/homePage/sportSegment2.json",
        SportSegment.class)


    InplayModule inplayModule = (InplayModule) inplayModuleConsumer.processModule(sportPageModule, null ,Collections.EMPTY_SET)
    Map<String, SegmentView> segmentWiseModules = new HashMap<>();
    inplayModuleConsumer.processSegmentwiseModules(
        inplayModule, segmentWiseModules, "InplayModule")
    SegmentView segmentView = new SegmentView()
    segmentWiseModules.put("segment",segmentView)
    Map<String, Set<Long>> segmentedExcludedEvents = new HashMap<>();
    Set<Long> eventIds = new HashSet<>();
    eventIds.add(6944787L);
    eventIds.add(8795185L);
    segmentedExcludedEvents.put("Universal", eventIds);

    when:
    inplayModuleConsumer.limitEvents(
        segmentWiseModules, inplayModule, segmentedExcludedEvents)
    then: "inplay module contains total number of segmentWiseModules"
    segmentWiseModules.size() == 4
  }
  def "test eventsByTypeName ordering"() {
    given: "cms inplay module configuaration"
    InPlayConfig cmsModuleConfig = TestUtils.deserializeWithGson("inplayModuleConsumer/homePage/cmsConfig.json",
        InPlayConfig.class)

    SportModule sportModule = new SportModule()
    sportModule.setSportId(0)
    sportModule.setId("aaa-bbb-ccc")

    SportPageModule sportPageModule = new SportPageModule(sportModule, Arrays.asList(cmsModuleConfig))

    and: "inplay data generation is 484"
    inplayDataService.getInplayDataVersion() >> "484"

    and: "inplay data is"
    inplayDataService.getInplayData("484") >> TestUtils.deserializeWithGson("inplayModuleConsumer/homePage/inplayData.json",
        InPlayData.class)

    and: "first sport segment in InplayData is Football"
    inplayDataService.getSportSegment("484", 16) >> TestUtils.deserializeWithGson("inplayModuleConsumer/homePage/sportSegment3.json",
        SportSegment.class)
    and: "second sport segment in InplayData is Tennis"
    inplayDataService.getSportSegment("484", 34) >> TestUtils.deserializeWithGson("inplayModuleConsumer/homePage/sportSegment2.json",
        SportSegment.class)

    and: "expected order is"
    def expectedOrder = [-34000, -31000, -30000]

    when:
    InplayModule inplayModule = (InplayModule) inplayModuleConsumer.processModule(sportPageModule, null,Collections.EMPTY_SET)
    def actualOrder = ((List<TypeSegment>) inplayModule.getData().get(0).getEventsByTypeName()).stream()
        .map { segment -> segment.getClassDisplayOrder() }
        .collect(Collectors.toList())

    then: "eventsByTypeName collection is orderded by classDisplayOrder"
    expectedOrder == actualOrder
  }

  def "test event exclusion works"() {
    given:
    Set<Long> excludedEvents = new HashSet<>()
    excludedEvents.add(6944787l)

    InPlayConfig cmsModuleConfig =
        TestUtils.deserializeWithGson("inplayModuleConsumer/sportPage/footballConfig.json",
        InPlayConfig.class)

    SportModule sportModule = new SportModule()
    sportModule.setSportId(34)
    sportModule.setId("aaa-bbb-ccc")

    SportPageModule sportPageModule = new SportPageModule(sportModule, Arrays.asList(cmsModuleConfig))

    and: "inplay data generation is 484"
    inplayDataService.getInplayDataVersion() >> "484"

    and: "sport segment is Football"
    inplayDataService.getSportSegment("484", 16) >>
        TestUtils.deserializeWithGson("inplayModuleConsumer/homePage/sportSegment1.json",
        SportSegment.class)

    when:
    InplayModule inplayModule = (InplayModule) inplayModuleConsumer.processModule(sportPageModule,null , excludedEvents)

    then:
    def typeSegment = inplayModule.getData().get(0)
        .getEventsByTypeName().get(0)

    and: "event-related fields are updated"
    typeSegment.getEvents().size() == 3
    typeSegment.getEventCount() == 3
    typeSegment.getEventsIds().contains(6950793l)
    typeSegment.getEventsIds().contains(8785876l)
    typeSegment.getEventsIds().contains(8788343l)
    !typeSegment.getEventsIds().contains(6944787l)

    and: "total count remains same, since it represents not only currently displayed events, but whole set of in-play for this sport"
    inplayModule.getTotalEvents() == 4
  }
}
