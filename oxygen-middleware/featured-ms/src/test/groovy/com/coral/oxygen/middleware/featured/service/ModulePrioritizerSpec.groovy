package com.coral.oxygen.middleware.featured.service

import com.coral.oxygen.middleware.featured.consumer.ModulePrioritizer
import com.coral.oxygen.middleware.pojos.model.cms.featured.SportModule
import com.coral.oxygen.middleware.pojos.model.cms.featured.SportPageModule
import com.coral.oxygen.middleware.pojos.model.output.featured.ModuleType
import spock.lang.Specification

import java.util.stream.Collectors

class ModulePrioritizerSpec extends Specification {

  def "verfify ordering"() {
    given:
    List<SportPageModule> list = new ArrayList<>()
    list.add(createModule(ModuleType.QUICK_LINK))
    list.add(createModule(ModuleType.FEATURED))
    list.add(createModule(ModuleType.HIGHLIGHTS_CAROUSEL))
    list.add(createModule(ModuleType.INPLAY))
    list.add(createModule(ModuleType.SURFACE_BET))

    when:
    List<SportPageModule> sortedList = list.stream()
        .sorted(ModulePrioritizer.SPORT_PAGE_MODULE_COMPARATOR).collect(Collectors.toList())

    then:
    getType(sortedList.get(0)) == ModuleType.HIGHLIGHTS_CAROUSEL
    getType(sortedList.get(1)) == ModuleType.INPLAY
    getType(sortedList.get(2)) == ModuleType.FEATURED
  }

  private SportPageModule createModule(ModuleType type) {
    SportModule sportModule = new SportModule()
    sportModule.setModuleType(type)
    return new SportPageModule(sportModule, new ArrayList<>())
  }

  private ModuleType getType(SportPageModule sportPageModule) {
    return sportPageModule.getSportModule().getModuleType();
  }
}
