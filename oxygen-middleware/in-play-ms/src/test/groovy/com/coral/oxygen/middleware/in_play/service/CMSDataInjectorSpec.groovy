package com.coral.oxygen.middleware.in_play.service

import com.coral.oxygen.middleware.pojos.model.InPlayTopLevelType
import com.coral.oxygen.middleware.pojos.model.cms.CmsInplayData
import com.coral.oxygen.middleware.pojos.model.output.inplay.InPlayData
import spock.lang.Specification

class CMSDataInjectorSpec extends Specification {

  CMSDataInjector injector

  def setup() {
    injector = new CMSDataInjector()
  }

  def cleanup() {
    injector = null
  }

  def "Test Inject Data: InPlay LiveNow" (){

    setup:
    CmsInplayData initialData = TestTools.initialDataFromFile("CMSDataInjectorTest/cmsData.json")
    InPlayData inPlayData = TestTools.inPlayDataFromFile("CMSDataInjectorTest/inPlayData.json")

    when:
    injector.injectData(inPlayData,  { -> initialData })

    then:
    def segment = inPlayData.getLivenow().getSportEvents().get(0)
    "sport/football" == segment.getSportUri()
    segment.isShowInPlay()
    "football" == segment.getCategoryPath()
    InPlayTopLevelType.LIVE_EVENT == segment.getTopLevelType()
  }
}
