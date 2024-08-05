package com.ladbrokescoral.oxygen.cms.api.service.sporttab

import com.ladbrokescoral.oxygen.cms.api.entity.SportTab
import spock.lang.Specification

class Tier2SportTabsTemplateSpec extends Specification{


  private Tier2SportTabsTemplate template;

  void setup() {
    template = new Tier2SportTabsTemplate()
  }

  private static SportTab createSportTab(String sportName) {
    return SportTab.builder()
        .name(sportName)
        .build()
  }

  def "get tabs by sport with ssCode=GOLF"() {

    given:
    def sportList = new ArrayList<SportTab>()
    sportList.add(createSportTab("GOLF"))
    template.getTabsBySport("GOLF") >> sportList
    when:
    def list = template.getTabsBySport("GOLF");
    then:
    !list.isEmpty()
  }

  def "get tabs by sport with ssCode!=GOLF"() {

    given:
    def sportList = new ArrayList<SportTab>()
    sportList.add(createSportTab("CURLING"))
    template.getTabsBySport("CURLING") >> sportList
    when:
    def list = template.getTabsBySport("CURLING");
    then:
    !list.isEmpty()
  }
}
