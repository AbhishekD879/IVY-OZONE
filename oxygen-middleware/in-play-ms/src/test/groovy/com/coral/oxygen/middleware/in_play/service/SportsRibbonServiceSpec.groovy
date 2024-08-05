package com.coral.oxygen.middleware.in_play.service

import com.coral.oxygen.middleware.pojos.model.cms.CmsInplayData
import com.coral.oxygen.middleware.pojos.model.cms.SportItem
import com.coral.oxygen.middleware.pojos.model.output.EventsModuleData
import com.coral.oxygen.middleware.pojos.model.output.inplay.*
import spock.lang.Specification

class SportsRibbonServiceSpec extends Specification {
  SportsRibbonService ribbonService

  def setup() {
    ribbonService = new SportsRibbonService()
  }

  def "Test creating sports ribbon by initial and inplay data" () {
    CmsInplayData initialData = TestTools.initialDataFromFile("CMSDataInjectorTest/cmsData.json")
    InPlayData inPlayData = TestTools.inPlayDataFromFile("SportsRibbonServiceTest/inPlayData.json")
    when:
    SportsRibbon ribbon = ribbonService.createSportsRibbon(initialData.getActiveSportCategories(), inPlayData)

    then:
    4 == ribbon.getItems().size()

    "ALL_SPORTS" == ribbon.getItems().get(0).getSsCategoryCode()

    "FOOTBALL" == ribbon.getItems().get(1).getCategoryCode()
    "Football" == ribbon.getItems().get(1).getCategoryName()
    ribbon.getItems().get(1).getHasLiveNow()
    ribbon.getItems().get(1).getHasUpcoming()
    14 == ribbon.getItems().get(1).getLiveEventCount()
    6 == ribbon.getItems().get(1).getUpcomingEventCount()

    "TENNIS" == ribbon.getItems().get(3).getCategoryCode()
    "Tennis" == ribbon.getItems().get(3).getCategoryName()
    ribbon.getItems().get(3).getHasLiveNow()
    !ribbon.getItems().get(3).getHasUpcoming()
    3 == ribbon.getItems().get(3).getLiveEventCount()
    0 == ribbon.getItems().get(3).getUpcomingEventCount()
  }

  def "Tests all sports has live now has upcoming"() {
    CmsInplayData initialData = TestTools.initialDataFromFile("CMSDataInjectorTest/cmsData.json")
    InPlayData inPlayData = TestTools.inPlayDataFromFile("SportsRibbonServiceTest/inPlayData.json")

    when:
    SportsRibbon ribbon = ribbonService.createSportsRibbon(initialData.getActiveSportCategories(), inPlayData)

    then:
    SportsRibbonItem allSports = ribbon.getItems().get(0)
    "ALL_SPORTS" == allSports.getSsCategoryCode()
    allSports.getHasLiveNow()
    allSports.getHasUpcoming()
  }

  def "Test all sports has no live now has no upcoming"() {
    CmsInplayData initialData = TestTools.initialDataFromFile("CMSDataInjectorTest/cmsData.json")
    InPlayData inPlayData = TestTools.inPlayDataFromFile("SportsRibbonServiceTest/inPlayData.json")
    inPlayData.getLivenow().getSportEvents().clear()
    inPlayData.getUpcoming().getSportEvents().clear()

    when:
    SportsRibbon ribbon = ribbonService.createSportsRibbon(initialData.getActiveSportCategories(), inPlayData)
    SportsRibbonItem allSports = ribbon.getItems().get(0)

    then:
    "ALL_SPORTS" == allSports.getSsCategoryCode()
    !allSports.getHasLiveNow()
    !allSports.getHasUpcoming()
    0 == allSports.getLiveEventCount()
    0 == allSports.getUpcomingEventCount()
  }

  def "Test all sports has live now has no upcoming"() {
    CmsInplayData initialData = TestTools.initialDataFromFile("CMSDataInjectorTest/cmsData.json")
    InPlayData inPlayData = TestTools.inPlayDataFromFile("SportsRibbonServiceTest/inPlayData.json")
    inPlayData.getUpcoming().getSportEvents().clear()

    when:
    SportsRibbon ribbon = ribbonService.createSportsRibbon(initialData.getActiveSportCategories(), inPlayData)
    SportsRibbonItem allSports = ribbon.getItems().get(0)

    then:
    "ALL_SPORTS" == allSports.getSsCategoryCode()
    allSports.getHasLiveNow()
    !allSports.getHasUpcoming()
    18 ==  allSports.getLiveEventCount()
    0 == allSports.getUpcomingEventCount()
  }

  def "Test all sports has no live now has upcoming"() {
    CmsInplayData initialData = TestTools.initialDataFromFile("CMSDataInjectorTest/cmsData.json")
    InPlayData inPlayData = TestTools.inPlayDataFromFile("SportsRibbonServiceTest/inPlayData.json")
    inPlayData.getLivenow().getSportEvents().clear()

    when:
    SportsRibbon ribbon = ribbonService.createSportsRibbon(initialData.getActiveSportCategories(), inPlayData)
    SportsRibbonItem allSports = ribbon.getItems().get(0)

    then:
    "ALL_SPORTS" == allSports.getSsCategoryCode()
    !allSports.getHasLiveNow()
    allSports.getHasUpcoming()
    0 == allSports.getLiveEventCount()
    6 == allSports.getUpcomingEventCount()
  }

  def "Test target uri calculation"() {
    CmsInplayData initialData = new CmsInplayData()
    initialData.setActiveSportCategories(new ArrayList<SportItem>())
    initialData.getActiveSportCategories().add(createSportItem("1", null))
    initialData.getActiveSportCategories().add(createSportItem("2", "a"))

    InPlayData data = new InPlayData()
    data.getLivenow().getSportEvents().add(createSportSegmentWithEvent(1, 1))
    data.getLivenow().getSportEvents().add(createSportSegmentWithEvent(2, 2))

    when:
    SportsRibbon sportsRibbon = ribbonService.createSportsRibbon(initialData.getActiveSportCategories(), data)

    then:
    null == sportsRibbon.getItems().get(0).getTargetUri()
    "#/in-play/a" == sportsRibbon.getItems().get(1).getTargetUri()
  }

  private static SportSegment createSportSegmentWithEvent(int categoryId, int displayOrder) {
    SportSegment sportSegment = new SportSegment()
    sportSegment.setCategoryId(categoryId)
    TypeSegment typeSegment = new TypeSegment()
    typeSegment.getEvents().add(new EventsModuleData())
    sportSegment.getEventsByTypeName().add(typeSegment)
    sportSegment.setDisplayOrder(displayOrder)
    return sportSegment
  }

  private static SportItem createSportItem(String categoryId, String targetUri) {
    SportItem sportItem = new SportItem()
    sportItem.setShowInPlay(true)
    sportItem.setCategoryId(categoryId)
    sportItem.setTargetUri(targetUri)
    return sportItem
  }
}
