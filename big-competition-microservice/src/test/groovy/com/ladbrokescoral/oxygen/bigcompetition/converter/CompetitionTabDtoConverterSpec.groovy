package com.ladbrokescoral.oxygen.bigcompetition.converter

import com.ladbrokescoral.oxygen.bigcompetition.TestUtil
import com.ladbrokescoral.oxygen.bigcompetition.dto.CompetitionTabDto
import com.ladbrokescoral.oxygen.bigcompetition.dto.module.CompetitionModuleDto
import com.ladbrokescoral.oxygen.bigcompetition.factory.ModuleServiceFactory
import com.ladbrokescoral.oxygen.bigcompetition.service.*
import com.ladbrokescoral.oxygen.cms.client.model.CompetitionModule
import com.ladbrokescoral.oxygen.cms.client.model.CompetitionTab
import spock.lang.Specification

class CompetitionTabDtoConverterSpec extends Specification {

  def 'test convert tab with modules'() {
    given:
    CompetitionSubTabDtoConverter subTabDtoConverter = Mock(CompetitionSubTabDtoConverter.class)
    subTabDtoConverter.convert(_ as List) >> Collections.emptyList()

    AemModuleService aemModuleService = Mock(AemModuleService.class)
    mockModuleService(aemModuleService)

    GroupModuleService groupModuleService = Mock(GroupModuleService.class)
    mockModuleService(groupModuleService)

    KnockoutModuleService knockoutModuleService = Mock(KnockoutModuleService.class)
    mockModuleService(knockoutModuleService)

    NextEventsModuleService nextEventsModuleService = Mock(NextEventsModuleService.class)
    mockModuleService(nextEventsModuleService)

    NextEventsIndividualModuleService nextEventsIndividualModuleService = Mock(NextEventsIndividualModuleService.class)
    mockModuleService(nextEventsIndividualModuleService)

    OutrightsModuleService outrightsModuleService = Mock(OutrightsModuleService.class)
    mockModuleService(outrightsModuleService)

    PromotionModuleService promotionModuleService = Mock(PromotionModuleService.class)
    mockModuleService(promotionModuleService)

    ResultModuleService resultModuleService = Mock(ResultModuleService.class)
    mockModuleService(resultModuleService)

    SpecialModuleService specialModuleService = Mock(SpecialModuleService.class)
    mockModuleService(specialModuleService)

    SurfaceBetsModuleService surfaceBetsModuleService = Mock(SurfaceBetsModuleService.class)
    mockModuleService(surfaceBetsModuleService)

    HighlightCarouselService highlightCarouselService = Mock(HighlightCarouselService.class)
    mockModuleService(highlightCarouselService)

    BybWidgetModuleService bybWidgetModuleService = Mock(BybWidgetModuleService.class)
    mockModuleService(bybWidgetModuleService)

    ModuleServiceFactory moduleServiceFactory = new ModuleServiceFactory(
        aemModuleService,
        groupModuleService,
        knockoutModuleService,
        nextEventsModuleService,
        nextEventsIndividualModuleService,
        outrightsModuleService,
        promotionModuleService,
        resultModuleService,
        specialModuleService,
        surfaceBetsModuleService,
        highlightCarouselService,
        bybWidgetModuleService)

    CompetitionModuleDtoConverter moduleDtoConverter = new CompetitionModuleDtoConverter(moduleServiceFactory)
    CompetitionTabDtoConverter converter = new CompetitionTabDtoConverter(subTabDtoConverter, moduleDtoConverter)

    and: "competitionTab that has came from cms-api"
    def competitionTab = TestUtil.deserializeWithJackson(
        "/converter/competitionTab.json", CompetitionTab.class)

    when:
    CompetitionTabDto tabDto = converter.convert(competitionTab)

    then: "tab should contain all modules except the ones with unknown type"
    tabDto.getCompetitionModules().size() == 15
  }

  CompetitionModuleDto createModuleDto() {
    return new CompetitionModuleDto() {
        }
  }

  void mockModuleService(ModuleService service) {
    service.process(_ as CompetitionModule) >> createModuleDto()
  }
}
