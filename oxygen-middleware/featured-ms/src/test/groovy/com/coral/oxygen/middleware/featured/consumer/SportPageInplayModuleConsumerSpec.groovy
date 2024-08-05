package com.coral.oxygen.middleware.featured.consumer

import com.coral.oxygen.middleware.featured.consumer.sportpage.InplayModuleConsumer
import com.coral.oxygen.middleware.featured.consumer.sportpage.ModuleConsumer
import com.coral.oxygen.middleware.featured.service.InplayDataService
import com.coral.oxygen.middleware.featured.service.injector.EventDataInjector
import com.coral.oxygen.middleware.featured.service.injector.FeaturedCommentaryInjector
import com.coral.oxygen.middleware.featured.utils.TestUtils
import com.coral.oxygen.middleware.pojos.model.cms.featured.InPlayConfig
import com.coral.oxygen.middleware.pojos.model.cms.featured.InplayDataSportItem
import com.coral.oxygen.middleware.pojos.model.cms.featured.SportModule
import com.coral.oxygen.middleware.pojos.model.cms.featured.SportPageModule
import com.coral.oxygen.middleware.pojos.model.output.EventsModuleData
import com.coral.oxygen.middleware.pojos.model.output.featured.InplayModule
import com.coral.oxygen.middleware.pojos.model.output.inplay.SportSegment
import com.coral.oxygen.middleware.pojos.model.output.inplay.TypeSegment
import spock.lang.Specification

class SportPageInplayModuleConsumerSpec extends Specification {

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

  def "build inplay module for sport page"() throws Exception {
    given: 'cms inplay module configuaration'
    InPlayConfig cmsModuleConfig = new InPlayConfig()
    cmsModuleConfig.setMaxEventCount(3)
    cmsModuleConfig.setSportId(16)
    def item = new InplayDataSportItem()
    item.eventCount = 5
    item.sportNumber = 16
    cmsModuleConfig.setHomeInplaySports(Arrays.asList(item))

    SportModule sportModule = new SportModule()
    sportModule.setSportId(16)
    sportModule.setId('aaa-bbb-ccc')

    SportPageModule sportPageModule = new SportPageModule(sportModule, Arrays.asList(cmsModuleConfig))

    and: 'inplay data generation is 484'
    inplayDataService.getInplayDataVersion() >> '484'

    and: 'sport with id = 16 is football'
    inplayDataService.getSportSegment('484', 16) >> TestUtils.deserializeWithGson('inplayModuleConsumer/sportPage/footballSportSegment.json',
        SportSegment.class)

    when:
    InplayModule inplayModule = (InplayModule) inplayModuleConsumer.processModule(sportPageModule, null, Collections.EMPTY_SET)

    then: 'inplay module contains only one football sport segment with id = 16'
    1 == inplayModule.getData().size()
    16 == inplayModule.getSportId()

    and: 'inplay module contains number of all football inplay events'
    25 == inplayModule.getTotalEvents()

    and: 'football sport segment contains 3 events as per cms configuration'
    SportSegment sportSegment = inplayModule.getData().get(0)
    3 == getEventsNumber(sportSegment)

    and: 'football sport segment have 2 types'
    2 == sportSegment.getEventsByTypeName().size()

    and: 'types are sorted by OB display order in ASC'
    TypeSegment firstType = sportSegment.getEventsByTypeName().get(0)
    TypeSegment secondType = sportSegment.getEventsByTypeName().get(1)
    firstType.getTypeDisplayOrder() <= secondType.getTypeDisplayOrder()

    and: 'events in type are sorted by OB start time in ASC'
    EventsModuleData firstEvent = firstType.getEvents().get(0)
    EventsModuleData secondEvent = firstType.getEvents().get(1)
    firstEvent.getStartTime() <= secondEvent.getStartTime()

    and: '2 events from first type'
    2 == firstType.getEventCount()
    8814082 == firstType.getEvents().get(0).getId()
    6950793 == firstType.getEvents().get(1).getId()

    and: '1 event from second type'
    1 == secondType.getEventCount()
    8813594 == secondType.getEvents().get(0).getId()
  }

  def "When total inplay events count is zero then module with error is returned"() {
    given:
    InPlayConfig cmsModuleConfig = new InPlayConfig()
    cmsModuleConfig.setMaxEventCount(0)
    cmsModuleConfig.setSportId(16)

    SportModule sportModule = new SportModule()
    sportModule.setSportId(16)
    sportModule.setId('aaa-bbb-ccc')

    SportPageModule sportPageModule = new SportPageModule(sportModule, Arrays.asList(cmsModuleConfig))

    when:
    InplayModule inplayModule = (InplayModule) inplayModuleConsumer.processModule(sportPageModule, null, Collections.EMPTY_SET)

    then:
    inplayModule.getErrorMessage() != null
  }

  def "When sum of inplay sports count is zero then module with error is returned"() {
    given:
    InPlayConfig cmsModuleConfig = new InPlayConfig()
    cmsModuleConfig.setMaxEventCount(5)
    cmsModuleConfig.setSportId(0)
    def item1 = new InplayDataSportItem()
    item1.sportNumber = 1
    item1.eventCount = 0
    def item2 = new InplayDataSportItem()
    item1.sportNumber = 2
    item1.eventCount = 0
    cmsModuleConfig.setHomeInplaySports(Arrays.asList(item1, item2))

    SportModule sportModule = new SportModule()
    sportModule.setSportId(16)
    sportModule.setId('aaa-bbb-ccc')

    SportPageModule sportPageModule = new SportPageModule(sportModule, Arrays.asList(cmsModuleConfig))

    when:
    InplayModule inplayModule = (InplayModule) inplayModuleConsumer.processModule(sportPageModule, null, Collections.EMPTY_SET)

    then:
    inplayModule.getErrorMessage() != null
  }

  int getEventsNumber(SportSegment sportSegment) {
    int count = 0
    sportSegment.getEventsByTypeName().each {
      count = count + it.getEvents().size()
    }
    return count
  }
}
