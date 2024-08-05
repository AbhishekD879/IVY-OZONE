package com.coral.oxygen.middleware.featured.consumer.sportpage

import com.coral.oxygen.cms.api.CmsService
import com.coral.oxygen.middleware.common.service.featured.OddsCardHeader
import com.coral.oxygen.middleware.featured.service.FeaturedDataFilter
import com.coral.oxygen.middleware.featured.service.injector.SingleOutcomeEventsModuleInjector
import com.coral.oxygen.middleware.pojos.model.cms.featured.*
import com.coral.oxygen.middleware.pojos.model.output.OutputMarket
import com.coral.oxygen.middleware.pojos.model.output.OutputPrice
import com.coral.oxygen.middleware.pojos.model.output.featured.ModuleType
import com.coral.oxygen.middleware.pojos.model.output.featured.SurfaceBetModule
import com.coral.oxygen.middleware.pojos.model.output.featured.SurfaceBetModuleData
import spock.lang.Specification

class SurfaceBetModuleProcessorTest extends Specification {

  SingleOutcomeEventsModuleInjector singleOutcomeDataInjector
  SurfaceBetModuleProcessor surfaceBetModuleProcessor
  OddsCardHeader oddsCardHeader
  FeaturedDataFilter featuredDataFilter
  def setup() {
    singleOutcomeDataInjector = Mock(SingleOutcomeEventsModuleInjector)
    oddsCardHeader = Mock(OddsCardHeader)
    featuredDataFilter = Mock(FeaturedDataFilter)
    surfaceBetModuleProcessor = new SurfaceBetModuleProcessor(singleOutcomeDataInjector, oddsCardHeader, featuredDataFilter)
  }

  def "Test converting SURFACE_BET sport page module to SurfaceBet EventModule"() {
    given:
    def surfaceBetCmsModule = createSurfaceBetCmsModule()
    def cmsSurfaceBets = listSurfaceBets()
    def sportPageModule = new SportPageModule(surfaceBetCmsModule, cmsSurfaceBets)
    singleOutcomeDataInjector.injectData(*_) >> { sb, idInjector ->
      (sb as List<SurfaceBetModuleData>).stream().forEach( {s ->
        def market = new OutputMarket()
        market.setPriceTypeCodes("SP")
        s.setMarkets(Arrays.asList(market))
      })
    }

    when:
    def actual = surfaceBetModuleProcessor.processModule(sportPageModule, null, null) as SurfaceBetModule

    then:
    actual.getId() == surfaceBetCmsModule.getId()
    actual.getTitle() == surfaceBetCmsModule.getTitle()
    actual.getSportId() == surfaceBetCmsModule.getSportId()
    Objects.nonNull(actual.getDisplayOrder())
    Objects.nonNull(actual.getData())
    actual.getData().size() == cmsSurfaceBets.size()
    SurfaceBetModuleData.class.isInstance(actual.getData().get(0))
  }

  def "Test converting SURFACE_BET sport page module to SurfaceBet EventModule Fanzone"() {
    given:
    def surfaceBetCmsModule = createSurfaceBetCmsModuleFanzone()
    def cmsSurfaceBets = listSurfaceBets()
    def sportPageModule = new SportPageModule(surfaceBetCmsModule, cmsSurfaceBets)
    surfaceBetModuleProcessor.setFanzonePageId("160")
    singleOutcomeDataInjector.injectData(_ as List, _, true) >> { sb, idInjector, displayed ->
      (sb as List<SurfaceBetModuleData>).stream().forEach( {s ->
        def market = new OutputMarket()
        market.setPriceTypeCodes("SP")
        s.setMarkets(Arrays.asList(market))
      })
    }

    when:
    def actual = surfaceBetModuleProcessor.processModule(sportPageModule, null, null) as SurfaceBetModule

    then:
    actual.getId() == surfaceBetCmsModule.getId()
    actual.getTitle() == surfaceBetCmsModule.getTitle()
    actual.getSportId() == surfaceBetCmsModule.getSportId()
    Objects.nonNull(actual.getDisplayOrder())
    Objects.nonNull(actual.getData())
    actual.getData().size() == cmsSurfaceBets.size()
    SurfaceBetModuleData.class.isInstance(actual.getData().get(0))
  }

  def "Test converting SURFACE_BET sport page module to SurfaceBet EventModule Fanzone1"() {
    given:
    def surfaceBetCmsModule = createSurfaceBetCmsModule()
    def cmsSurfaceBets = listSurfaceBets()
    def sportPageModule = new SportPageModule(surfaceBetCmsModule, cmsSurfaceBets)
    surfaceBetModuleProcessor.setFanzonePageId("160")
    singleOutcomeDataInjector.injectData(_ as List, _, true) >> { sb, idInjector, displayed ->
      (sb as List<SurfaceBetModuleData>).stream().forEach( {s ->
        def market = new OutputMarket()
        market.setPriceTypeCodes("SP")
        s.setMarkets(Arrays.asList(market))
      })
    }

    when:
    def actual = surfaceBetModuleProcessor.processModule(sportPageModule, null, null) as SurfaceBetModule

    then:
    actual.getId() == surfaceBetCmsModule.getId()
    actual.getTitle() == surfaceBetCmsModule.getTitle()
    actual.getSportId() == surfaceBetCmsModule.getSportId()
    Objects.nonNull(actual.getDisplayOrder())
    Objects.nonNull(actual.getData())
  }

  def "Test SURFACE_BET without prices and LP market are filtered out"() {
    given:
    def surfaceBetCmsModule = createSurfaceBetCmsModule()
    def cmsSurfaceBets = listSurfaceBets()
    def sportPageModule = new SportPageModule(surfaceBetCmsModule, cmsSurfaceBets)
    singleOutcomeDataInjector.injectData(*_) >> { sb, idInjector ->
      (sb as List<SurfaceBetModuleData>).stream().forEach( {s ->
        def market = new OutputMarket()
        market.setPriceTypeCodes("LP")
        s.setMarkets(Arrays.asList(market))
      })
    }

    when:
    def actual = surfaceBetModuleProcessor.processModule(sportPageModule, null, null) as SurfaceBetModule

    then:
    Objects.nonNull(actual.getData())
    actual.getData().size() == 0
  }

  def "Test SurfaceBets Module postprocess without data"() {
    given:
    def surfaceBetModule = new SurfaceBetModule()
    surfaceBetModule.setData(Collections.emptyList())

    when:
    def module = surfaceBetModuleProcessor.postProcessModule(surfaceBetModule)

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
    def module = surfaceBetModuleProcessor.postProcessModule(surfaceBetModule)

    then:
    module.getOutcomeColumnsTitles().equals(outcomeTitles)
    module.hasNoLiveEvents()
    SurfaceBetModuleData surfaceBetModuleData= module.getData().get(0);
    surfaceBetModuleData.getSvgBgId().equals("image1")
    surfaceBetModuleData.getSvgBgImgPath().equals("test1.svg")
    surfaceBetModuleData.getContentHeader().equals("test")
    Boolean.TRUE.equals(module.getCashoutAvail())
  }

  List<SportPageModuleDataItem> listSurfaceBets() {
    def surfaceBet = new SurfaceBet()
    surfaceBet.setTitle("SB title")
    surfaceBet.setType(ModuleType.SURFACE_BET.name())
    surfaceBet.setSelectionId(12345)
    surfaceBet.setPrice(new OutputPrice())
    surfaceBet.setDisplayOnDesktop(true)
    surfaceBet.setSvgBgId("image1")
    surfaceBet.setSvgBgImgPath("test1.svg")
    surfaceBet.setContentHeader("test")
    Arrays.asList(surfaceBet)
  }

  SportModule createSurfaceBetCmsModule() {
    def module = new SportModule()
    module.setBrand("bma")
    module.setModuleType(ModuleType.SURFACE_BET)
    module.setSortOrder(0)
    module.setTitle("SB Module title")
    module.setSportId(0)
    module
  }

  SportModule createSurfaceBetCmsModuleFanzone() {
    def module = new SportModule()
    module.setBrand("bma")
    module.setModuleType(ModuleType.SURFACE_BET)
    module.setSortOrder(0)
    module.setTitle("SB Module title")
    module.setSportId(160)
    module.setPageId("160")
    module
  }

  SurfaceBetModuleData createSurfaceBetModuleData() {
    def module = new SurfaceBetModuleData();
    module.setTitle("SB Module title")
    module.setSvgBgId("image1")
    module.setSvgBgImgPath("test1.svg")
    module.setContentHeader("test")
    module
  }
}
