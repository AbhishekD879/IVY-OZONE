package com.ladbrokescoral.oxygen.cms.api.service.sporttab

import com.ladbrokescoral.oxygen.cms.api.entity.SportTab
import com.ladbrokescoral.oxygen.cms.api.repository.PopularTabRepository
import com.ladbrokescoral.oxygen.cms.api.repository.SportTabRepository
import com.ladbrokescoral.oxygen.cms.api.repository.TrendingTabRepository
import org.springframework.util.ObjectUtils
import spock.lang.Specification

class SportTabServiceSpec extends Specification {
  private SportTabRepository repository
  private TrendingTabRepository trendingTabRepository;
  private PopularTabRepository popularTabRepository;
  private SportTabService service

  void setup() {
    repository = Mock(SportTabRepository)
    trendingTabRepository = Mock(TrendingTabRepository)
    popularTabRepository = Mock(PopularTabRepository)
    service = new SportTabService(repository, null, trendingTabRepository, popularTabRepository)
  }

  def "If checkEvents=true then entity is save only when hasEvents is changed"() {
    when:
    repository.findAllByBrandAndSportIdAndName("bma", 16, "competitions") >>
        [sportTab(true, false)]
    service.updateHasEvents("bma", 16, SportTabNames.COMPETITIONS, true)
    then:
    1 * repository.save(_) >> { args -> validateSportTab(args[0], true)}

    when:
    repository.findAllByBrandAndSportIdAndName("bma", 16, "competitions") >>
        [sportTab(true, true)]
    service.updateHasEvents("bma", 16, SportTabNames.COMPETITIONS, false)
    then:
    1 * repository.save(_) >> { args ->  validateSportTab(args[0], false)}

    when:
    repository.findAllByBrandAndSportIdAndName("bma", 16, "competitions") >>
        [sportTab(true, true)]
    service.updateHasEvents("bma", 16, SportTabNames.COMPETITIONS, true)
    then:
    0 * repository.save(_)

    when:
    repository.findAllByBrandAndSportIdAndName("bma", 16, "competitions") >>
        [sportTab(true, false)]
    service.updateHasEvents("bma", 16, SportTabNames.COMPETITIONS, false)
    then:
    0 * repository.save(_)
  }

  private static void validateSportTab(sportTab, shouldHasEvents) {
    def tab = sportTab as SportTab
    assert !ObjectUtils.isEmpty(tab.getId())
    assert tab.isHasEvents() == shouldHasEvents
  }

  def "If checkEvents=false then sportTab isn't updated"() {
    when:
    repository.findAllByBrandAndSportIdAndName("bma", 16, "competitions") >>
        [sportTab(false, false)]

    service.updateHasEvents("bma", 16, SportTabNames.COMPETITIONS, true)
    then:
    0 * repository.save(_)
  }

  def "disable checkEvents for live tab"() {
    when:
    SportTab tab = service.prepareModelBeforeSave(sportTab("live", true))
    then:
    !tab.checkEvents

    when:
    tab = service.prepareModelBeforeSave(sportTab("matches", true))
    then:
    tab.checkEvents

    when:
    tab = service.prepareModelBeforeSave(sportTab("outrights", true))
    then:
    tab.checkEvents

    when:
    tab = service.prepareModelBeforeSave(sportTab("coupons", true))
    then:
    tab.checkEvents
  }

  private static SportTab sportTab(boolean checkEvents, boolean hasEvents) {
    return SportTab.builder()
        .id("id is present")
        .checkEvents(checkEvents)
        .hasEvents(hasEvents)
        .build()
  }

  private static SportTab sportTab(String name, boolean checkEvents) {
    return SportTab.builder()
        .checkEvents(checkEvents)
        .name(name)
        .build()
  }
}
