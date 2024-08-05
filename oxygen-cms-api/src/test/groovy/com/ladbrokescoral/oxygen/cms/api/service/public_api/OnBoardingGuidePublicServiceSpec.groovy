package com.ladbrokescoral.oxygen.cms.api.service.public_api


import com.ladbrokescoral.oxygen.cms.api.entity.OnBoardingGuide
import com.ladbrokescoral.oxygen.cms.api.service.OnBoardingGuideService
import spock.lang.Specification

class OnBoardingGuidePublicServiceSpec extends Specification {

  public static final String BMA = "bma"

  def "GetOnBoardingGuides"() {
    given:
    List<OnBoardingGuide> items = new ArrayList<>()
    OnBoardingGuide onBoardingGuide = new OnBoardingGuide()
    onBoardingGuide.setBrand(BMA)
    onBoardingGuide.setGuidePath("/test/path")
    onBoardingGuide.setEnabled(true)
    items.add(onBoardingGuide)
    onBoardingGuide = new OnBoardingGuide()
    onBoardingGuide.setBrand(BMA)
    onBoardingGuide.setGuidePath("/test2/path")
    onBoardingGuide.setEnabled(false)
    items.add(onBoardingGuide)
    OnBoardingGuideService privateService = Mock(OnBoardingGuideService)
    privateService.findByBrand(BMA) >> items

    when:
    OnBoardingGuidePublicService service = new OnBoardingGuidePublicService(privateService)
    def guides = service.getOnBoardingGuides(BMA)

    then:
    guides.size() == 1
  }
}
