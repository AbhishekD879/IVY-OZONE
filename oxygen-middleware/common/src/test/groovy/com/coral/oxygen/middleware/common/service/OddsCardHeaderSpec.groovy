package com.coral.oxygen.middleware.common.service

import com.coral.oxygen.middleware.common.service.featured.OddsCardHeader
import com.coral.oxygen.middleware.pojos.model.output.EventsModuleData
import com.coral.oxygen.middleware.pojos.model.output.OutputMarket
import com.coral.oxygen.middleware.pojos.model.output.featured.EventsModule
import com.coral.oxygen.middleware.pojos.model.output.OutputOutcome
import spock.lang.Specification

class OddsCardHeaderSpec extends Specification {

  OddsCardHeader oddsCardHeader

  SportsConfig sportsConfig
  OutrightsConfig outrightsConfig

  EventsModule eventsModule

  def setup() {
    oddsCardHeader = new OddsCardHeader()

    sportsConfig = Mock(SportsConfig)
    SportsConfig.SportConfigItem sportsConfigItem =
        new SportsConfig.ItemBuilder('key', 'id').setSpecialsTypeIds('1', '2').build()
    sportsConfig.getBySportId(_) >> new SportsConfig.SportConfigItem()
    sportsConfig.getByName(_) >> sportsConfigItem

    oddsCardHeader.setSportsConfig(sportsConfig)
    outrightsConfig = Mock(OutrightsConfig)
    outrightsConfig.getOutrightsSports() >> Arrays.asList('Sport1', 'Sport2')
    outrightsConfig.getSportSortCode() >> Arrays.asList('TNMT', 'TR01', 'TR02')

    oddsCardHeader.setOutrightsConfig(outrightsConfig)

    eventsModule = prepareOutputModule()
  }

  def "Verify 1_2 headTitles for module"() {
    when:
    List<String> actualTitles = oddsCardHeader.calculateHeadTitles(eventsModule.getData())

    then:
    OddsCardHeader.L_1_2 == actualTitles
  }

  def "Verify OVER_UNDER headTitles for module"() {
    eventsModule.getData().forEach({ dataItem ->
      dataItem.getMarkets().forEach({ market ->
        market.setMarketMeaningMajorCode('L')
      })
    })
    eventsModule.getData().get(0).getMarkets().get(0).setOutcomes(Arrays.asList(new OutputOutcome()))

    when:
    List<String> actualTitles = oddsCardHeader.calculateHeadTitles(eventsModule.getData())

    then:
    OddsCardHeader.L_OVER_UNDER == actualTitles
  }

  def "Verify HOME_AWAY headTitles for module"() {
    eventsModule.getData().get(0).getMarkets().get(0).setOutcomes(Arrays.asList(new OutputOutcome()))

    when:
    List<String> actualTitles = oddsCardHeader.calculateHeadTitles(eventsModule.getData())

    then:
    OddsCardHeader.L_HOME_AWAY == actualTitles
  }

  def "Verify HOME_DRAW_AWAY headTitles for module"() {
    eventsModule.getData().forEach({ dataItem ->
      dataItem.getMarkets().forEach({ market ->
        // makes market of match result type
        market.setMarketMeaningMajorCode('-')
        market.setMarketMeaningMinorCode('MR')
      })
    })
    eventsModule.getData().get(0).getMarkets().get(0).setOutcomes(Arrays.asList(new OutputOutcome()))

    when:
    List<String> actualTitles = oddsCardHeader.calculateHeadTitles(eventsModule.getData())

    then:
    OddsCardHeader.L_HOME_DRAW_AWAY == actualTitles
  }

  def "Verify YES_NO headTitles for module"() {
    eventsModule.getData().forEach({ dataItem ->
      dataItem.getMarkets().forEach({ market ->
        market.setDispSortName('GB')
      })
    })
    eventsModule.getData().get(0).getMarkets().get(0).setOutcomes(Arrays.asList(new OutputOutcome()))

    when:
    List<String> actualTitles = oddsCardHeader.calculateHeadTitles(eventsModule.getData())

    then:
    OddsCardHeader.L_YES_NO == actualTitles
  }

  def "Verify 1_2_3 headTitles for module"() {
    SportsConfig.SportConfigItem sportsConfigItem =
        new SportsConfig.ItemBuilder('key', 'id')
        .setSpecialsTypeIds('1', '2')
        .setOddsCardHeaderType(OddsCardHeaderType.oneThreeType)
        .build()

    when:
    List<String> actualTitles = oddsCardHeader.calculateHeadTitles(eventsModule.getData())

    then:
    sportsConfig.getByName(_) >> sportsConfigItem
    OddsCardHeader.L_1_2_3 == actualTitles
  }

  def "Head title is null for Special events"() {
    SportsConfig.SportConfigItem sportConfigItem = Mock(SportsConfig.SportConfigItem)
    // setting condition for "Special event"
    sportConfigItem.isRacing() >> true

    when:
    List<String> actualTitles = oddsCardHeader.calculateHeadTitles(eventsModule.getData())

    then:
    sportsConfig.getBySportId(_) >> sportConfigItem
    actualTitles == null
  }

  private EventsModule prepareOutputModule() {
    List<EventsModuleData> data = new ArrayList<EventsModuleData>()
    data.add(prepareModuleDataItem())

    eventsModule = new EventsModule()
    eventsModule.setData(data)

    return eventsModule
  }

  private EventsModuleData prepareModuleDataItem() {
    List<OutputMarket> outputMarkets = new ArrayList<OutputMarket>()
    outputMarkets.add(prepareOutputMarket())

    EventsModuleData moduleDataItem = new EventsModuleData()
    moduleDataItem.setMarkets(outputMarkets)
    moduleDataItem.setCategoryName('football')
    moduleDataItem.setCategoryCode('CategoryCode')
    moduleDataItem.setCategoryId('CategoryId')

    return moduleDataItem
  }

  private OutputMarket prepareOutputMarket() {
    OutputMarket outputMarket = new OutputMarket()
    outputMarket.setMarketMeaningMajorCode('Major')
    outputMarket.setMarketMeaningMinorCode('Minor')

    return outputMarket
  }
}
