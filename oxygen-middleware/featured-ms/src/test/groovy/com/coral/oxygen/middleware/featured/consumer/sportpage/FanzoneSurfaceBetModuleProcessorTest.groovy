package com.coral.oxygen.middleware.featured.consumer.sportpage

import com.coral.oxygen.cms.api.CmsService
import com.coral.oxygen.middleware.common.service.featured.OddsCardHeader
import com.coral.oxygen.middleware.featured.service.FeaturedDataFilter
import com.coral.oxygen.middleware.featured.service.injector.SingleOutcomeEventsModuleInjector
import com.coral.oxygen.middleware.pojos.model.cms.Fanzone
import com.coral.oxygen.middleware.pojos.model.cms.featured.*
import com.coral.oxygen.middleware.pojos.model.output.OutputMarket
import com.coral.oxygen.middleware.pojos.model.output.OutputPrice
import com.coral.oxygen.middleware.pojos.model.output.featured.ModuleType
import com.coral.oxygen.middleware.pojos.model.output.featured.SurfaceBetModule
import com.coral.oxygen.middleware.pojos.model.output.featured.SurfaceBetModuleData
import spock.lang.Specification

class FanzoneSurfaceBetModuleProcessorTest extends Specification {

  SingleOutcomeEventsModuleInjector singleOutcomeDataInjector
  FanzoneSurfaceBetModuleProcessor fanzoneSurfaceBetModuleProcessor
  OddsCardHeader oddsCardHeader
  FeaturedDataFilter featuredDataFilter
  CmsService cmsService
  def setup() {
    singleOutcomeDataInjector = Mock(SingleOutcomeEventsModuleInjector)
    oddsCardHeader = Mock(OddsCardHeader)
    featuredDataFilter = Mock(FeaturedDataFilter)
    cmsService = Mock(CmsService)
    fanzoneSurfaceBetModuleProcessor = new FanzoneSurfaceBetModuleProcessor(singleOutcomeDataInjector, oddsCardHeader, featuredDataFilter,cmsService)
  }

  def "Test converting SURFACE_BET sport page module to SurfaceBet EventModule"() {
    given:
    def surfaceBetCmsModule = createSurfaceBetCmsModule()
    def cmsSurfaceBets = listSurfaceBets()
    def sportPageModule = new SportPageModule(surfaceBetCmsModule, cmsSurfaceBets)
    def fanzone1 = new Fanzone()
    fanzone1.name = "segment-one"
    fanzone1.primaryCompetitionId = "441"
    fanzone1.secondaryCompetitionId = "442,443"
    fanzone1.teamId = "1234"
    def fanzone2 = new Fanzone()
    fanzone2.name = "segment-two"
    fanzone2.primaryCompetitionId = "441"
    fanzone2.secondaryCompetitionId = "442,443"
    fanzone2.teamId = "12345"
    def fanzones = Arrays.asList(fanzone1,fanzone2)
    cmsService.getFanzones() >> fanzones
    singleOutcomeDataInjector.injectData(*_) >> { sb, idInjector ->
      (sb as List<SurfaceBetModuleData>).stream().forEach( {s ->
        def market = new OutputMarket()
        market.setPriceTypeCodes("SP")
        s.setMarkets(Arrays.asList(market))
      })
    }

    when:
    def actual = fanzoneSurfaceBetModuleProcessor.processModule(sportPageModule, null, null) as SurfaceBetModule

    then:
    actual.getId() == surfaceBetCmsModule.getId()
    actual.getTitle() == surfaceBetCmsModule.getTitle()
    actual.getSportId() == surfaceBetCmsModule.getSportId()
    Objects.nonNull(actual.getDisplayOrder())
    Objects.nonNull(actual.getData())
    actual.getData().size() == cmsSurfaceBets.size()
    SurfaceBetModuleData.class.isInstance(actual.getData().get(0))
  }

  def "Test SURFACE_BET without prices and LP market are filtered out"() {
    given:
    def surfaceBetCmsModule = createSurfaceBetCmsModule()
    def cmsSurfaceBets = listSurfaceBets()
    def sportPageModule = new SportPageModule(surfaceBetCmsModule, cmsSurfaceBets)
    def fanzone1 = new Fanzone()
    fanzone1.name = "segment-one"
    fanzone1.primaryCompetitionId = "441"
    fanzone1.secondaryCompetitionId = "442,443"
    fanzone1.teamId = "1234"
    def fanzone2 = new Fanzone()
    fanzone2.name = "segment-two"
    fanzone2.primaryCompetitionId = "441"
    fanzone2.secondaryCompetitionId = "442,443"
    fanzone2.teamId = "12345"
    def fanzone3 = new Fanzone()
    fanzone3.name = "invalid"
    fanzone3.primaryCompetitionId = "441"
    fanzone3.secondaryCompetitionId = "442,443"
    fanzone3.teamId = "12345"
    def fanzones = Arrays.asList(fanzone1,fanzone2,fanzone3)
    cmsService.getFanzones() >> fanzones
    singleOutcomeDataInjector.injectData(*_) >> { sb, idInjector ->
      (sb as List<SurfaceBetModuleData>).stream().forEach( {s ->
        def market = new OutputMarket()
        market.setPriceTypeCodes("LP")
        s.setMarkets(Arrays.asList(market))
      })
    }

    when:
    def actual = fanzoneSurfaceBetModuleProcessor.processModule(sportPageModule, null, null) as SurfaceBetModule

    then:
    Objects.nonNull(actual.getData())
    actual.getData().size() == 0
  }

  def "Test SurfaceBets Module postprocess without data"() {
    given:
    def surfaceBetModule = new SurfaceBetModule()
    surfaceBetModule.setData(Collections.emptyList())

    when:
    def module = fanzoneSurfaceBetModuleProcessor.postProcessModule(surfaceBetModule)

    then:
    module.getOutcomeColumnsTitles() == null || module.getOutcomeColumnsTitles().isEmpty()
    module.hasNoLiveEvents()
    Objects.isNull(module.getCashoutAvail())
  }

  def "Test SurfaceBets Module postprocess"() {
    given:
    def surfaceBetModule = new SurfaceBetModule()
    surfaceBetModule.setData(Collections.singletonList(createSurfaceBetModuleData()))
    def outcomeTitles = Arrays.asList("1", "2", "3")
    oddsCardHeader.calculateHeadTitles(_) >> outcomeTitles
    featuredDataFilter.isCashOutAvailable(_) >> true

    when:
    def module = fanzoneSurfaceBetModuleProcessor.postProcessModule(surfaceBetModule)

    then:
    module.getOutcomeColumnsTitles().equals(outcomeTitles)
    module.hasNoLiveEvents()
    SurfaceBetModuleData surfaceBetModuleData= module.getData().get(0);
    Boolean.TRUE.equals(module.getCashoutAvail())
  }

  List<SportPageModuleDataItem> listSurfaceBets() {
    def fanzones = Arrays.asList("1234", "12345")
    def surfaceBet = new SurfaceBet()
    surfaceBet.setTitle("SB title")
    surfaceBet.setType(ModuleType.SURFACE_BET.name())
    surfaceBet.setSelectionId(12345)
    surfaceBet.setPrice(new OutputPrice())
    surfaceBet.setFanzoneSegments(fanzones)
    Arrays.asList(surfaceBet)
  }

  SportModule createSurfaceBetCmsModule() {
    def module = new SportModule()
    module.setBrand("bma")
    module.setModuleType(ModuleType.SURFACE_BET)
    module.setSortOrder(0)
    module.setTitle("SB Module title")
    module.setSportId(160)
    module
  }
  SurfaceBetModuleData createSurfaceBetModuleData() {
    def module = new SurfaceBetModuleData();
    module.setTitle("SB Module title")
    module
  }
}
