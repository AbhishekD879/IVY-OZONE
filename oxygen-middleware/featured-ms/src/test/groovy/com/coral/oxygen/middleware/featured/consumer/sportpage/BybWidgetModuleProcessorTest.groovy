package com.coral.oxygen.middleware.featured.consumer.sportpage


import com.coral.oxygen.middleware.featured.service.injector.EventDataInjector
import com.coral.oxygen.middleware.pojos.model.cms.featured.*
import com.coral.oxygen.middleware.pojos.model.output.OutputMarket
import com.coral.oxygen.middleware.pojos.model.output.featured.BybWidgetModule
import com.coral.oxygen.middleware.pojos.model.output.featured.BybWidgetModuleData
import com.coral.oxygen.middleware.pojos.model.output.featured.FeaturedRawIndex
import com.coral.oxygen.middleware.pojos.model.output.featured.ModuleType
import spock.lang.Specification

class BybWidgetModuleProcessorTest extends Specification {

  EventDataInjector eventDataInjector
  BybWidgetProcessor bybWidgetProcessor

  def setup() {
    eventDataInjector = Mock(EventDataInjector)

    bybWidgetProcessor = new BybWidgetProcessor(eventDataInjector)
  }

  def "Test converting BYB_WIDGET sport page module to bybWidget EventModule"() {
    given:
    def sportPageModule = cretaeSportModule()
    eventDataInjector.injectData(*_) >> { sb, idInjector ->
      (sb as List<BybWidgetModuleData>).stream().forEach( { s ->
        def market = new OutputMarket()
        market.setPriceTypeCodes("SP")
        market.setId("47897634")

        def market1 = new OutputMarket()
        market1.setPriceTypeCodes("SP")
        market1.setId("47897635")
        s.setPrimaryMarkets(Arrays.asList(market,market1))
        s.setId(57124358)
      })
    }

    when:
    def actual = bybWidgetProcessor.processModule(sportPageModule, null, null) as BybWidgetModule

    then:
    actual.getId() == sportPageModule.getSportModule().getId()
    actual.getTitle() == sportPageModule.getSportModule().getTitle()
    actual.getSportId() == sportPageModule.getSportModule().getSportId()
    Objects.nonNull(actual.getDisplayOrder())
    Objects.nonNull(actual.getData())
    actual.getData().size() == 2
    BybWidgetModuleData.class.isInstance(actual.getData().get(0))
  }



  private SportPageModule cretaeSportModule() {
    SportModule module =
        new SportModule(
        FeaturedRawIndex.PageType.sport,
        "123",
        0,
        0.0,
        true,
        "0",
        "title",
        "ladbrokes",
        ModuleType.BYB_WIDGET,
        new ArrayList<>());
    List<SportPageModuleDataItem> widgetModule = createBYbWwidget();
    SportPageModule sportPageModule = new SportPageModule(module, widgetModule);
    return sportPageModule;
  }

  private List<SportPageModuleDataItem> createBYbWwidget() {
    BybWidget widget = new BybWidget();

    widget.setId("12313131");
    widget.setTitle("title");
    widget.setShowAll(true);
    widget.setMarketCardVisibleSelections(1);
    widget.setPageType(FeaturedRawIndex.PageType.sport);
    widget.setData(prepareWidgetData());
    List<SportPageModuleDataItem> list = new ArrayList<>();
    list.add(widget);
    return list;
  }

  private List<BybWidgetData> prepareWidgetData() {
    List<BybWidgetData> widgets = new ArrayList<>();
    widgets.add(createWidgetData("title-2", "47897633", "57124357", 2));
    widgets.add(createWidgetData("title-3", "47897634", "57124358", 3));
    widgets.add(createWidgetData("title-4", "47897635", "57124358", 4));
    widgets.add(createWidgetData("title-5", "47897636", "57124358", 5));

    return widgets;
  }

  private BybWidgetData createWidgetData(
      String title, String marketId, String eventId, int sortOrder) {
    BybWidgetData data = new BybWidgetData();
    data.setTitle(title);
    data.setMarketId(marketId);
    data.setEventId(eventId);
    data.setSortOrder(sortOrder);
    return data;
  }
}
