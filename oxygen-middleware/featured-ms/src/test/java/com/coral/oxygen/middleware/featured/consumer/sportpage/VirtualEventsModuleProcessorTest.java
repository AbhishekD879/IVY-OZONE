package com.coral.oxygen.middleware.featured.consumer.sportpage;

import static com.coral.oxygen.middleware.featured.consumer.sportpage.virtual.VirtualEventsModuleProcessor.TWO_UP_MARKET;
import static com.coral.oxygen.middleware.featured.utils.FeaturedDataUtils.getSSEventToOutcomeForOutcome;

import com.coral.oxygen.middleware.common.configuration.GsonConfiguration;
import com.coral.oxygen.middleware.common.service.SportsConfig;
import com.coral.oxygen.middleware.featured.consumer.sportpage.virtual.VirtualEventsModuleProcessor;
import com.coral.oxygen.middleware.featured.service.injector.VirtualEventDataInjector;
import com.coral.oxygen.middleware.pojos.model.cms.featured.SportModule;
import com.coral.oxygen.middleware.pojos.model.cms.featured.SportPage;
import com.coral.oxygen.middleware.pojos.model.cms.featured.SportPageModule;
import com.coral.oxygen.middleware.pojos.model.cms.featured.SportPageModuleDataItem;
import com.coral.oxygen.middleware.pojos.model.cms.featured.VirtualEvent;
import com.coral.oxygen.middleware.pojos.model.output.EventsModuleData;
import com.coral.oxygen.middleware.pojos.model.output.OutputMarket;
import com.coral.oxygen.middleware.pojos.model.output.featured.AbstractFeaturedModule;
import com.coral.oxygen.middleware.pojos.model.output.featured.FeaturedRawIndex;
import com.coral.oxygen.middleware.pojos.model.output.featured.HighlightCarouselModule;
import com.coral.oxygen.middleware.pojos.model.output.featured.ModuleType;
import com.coral.oxygen.middleware.pojos.model.output.featured.VirtualEventModule;
import com.egalacoral.spark.siteserver.model.Event;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import org.junit.Assert;
import org.junit.Test;
import org.junit.jupiter.api.Assertions;
import org.junit.runner.RunWith;
import org.mockito.Mockito;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.context.properties.EnableConfigurationProperties;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.test.context.junit4.SpringJUnit4ClassRunner;

@EnableConfigurationProperties
@RunWith(SpringJUnit4ClassRunner.class)
@SpringBootTest(
    classes = {SportsConfig.class, GsonConfiguration.class, VirtualEventsModuleProcessor.class})
public class VirtualEventsModuleProcessorTest {

  @Autowired VirtualEventsModuleProcessor virtualEventsModuleProcessor;

  @MockBean VirtualEventDataInjector virtualEventDataInjector;

  @Test
  public void processModuleTestForException() {
    Assert.assertThrows(
        UnsupportedOperationException.class,
        () -> virtualEventsModuleProcessor.processModule(null, null, null));
  }

  @Test
  public void processModulesForException() {

    Mockito.doThrow(new IllegalArgumentException())
        .when(virtualEventDataInjector)
        .injectDataEvents(Mockito.any());
    Assertions.assertDoesNotThrow(
        () ->
            virtualEventsModuleProcessor.processModules(
                virtualEventswithEventIds().getSportPageModules().get(0), null, null));
  }

  @Test
  public void processModulesForLiveEvents() {

    Assertions.assertDoesNotThrow(
        () ->
            virtualEventsModuleProcessor.processModules(
                virtualEventswithEventIds().getSportPageModules().get(0), null, null));
  }

  @Test
  public void processModulesForFinishedEvents() {

    Assertions.assertDoesNotThrow(
        () ->
            virtualEventsModuleProcessor.processModules(
                virtualEventswithEventIds().getSportPageModules().get(0), null, null));
  }

  @Test
  public void applyLimitsWithNoExceptoin() {

    Assertions.assertDoesNotThrow(
        () -> virtualEventsModuleProcessor.applyLimits(getVirtualEventModule()));
  }

  @Test
  public void applyLimitsMoreThanLimitWithNoExceptoin() {
    List<AbstractFeaturedModule<?>> modules = getVirtualEventModule();
    ((VirtualEventModule) modules.get(0)).setLimit(30);
    Assertions.assertDoesNotThrow(() -> virtualEventsModuleProcessor.applyLimits(modules));
  }

  @Test
  public void applyLimitsMoreThanLimitEqualsToZeroNoExceptoin() {
    List<AbstractFeaturedModule<?>> modules = getVirtualEventModule();
    modules.addAll(getVirtualEventModule());
    modules.addAll(getVirtualEventModule());
    modules.addAll(getVirtualEventModule());
    modules.addAll(getVirtualEventModule());
    modules.addAll(getVirtualEventModule());
    modules.addAll(getVirtualEventModule());
    modules.addAll(getVirtualEventModule());
    modules.addAll(getVirtualEventModule());
    modules.addAll(getVirtualEventModule());
    modules.addAll(getVirtualEventModule());
    modules.addAll(getVirtualEventModule());
    modules.addAll(getVirtualEventModule());
    modules.add(new HighlightCarouselModule());
    ((VirtualEventModule) modules.get(1)).setLimit(2);
    Assertions.assertDoesNotThrow(() -> virtualEventsModuleProcessor.applyLimits(modules));
  }

  @Test
  public void applyLimitsLessThanLimitWithNoExceptoin() {
    List<AbstractFeaturedModule<?>> modules = getVirtualEventModule();
    ((VirtualEventModule) modules.get(0)).setLimit(2);
    Assertions.assertDoesNotThrow(() -> virtualEventsModuleProcessor.applyLimits(modules));
  }

  @Test
  public void applyLimitsWithInconsistencyValues() {
    List<AbstractFeaturedModule<?>> modules = getVirtualEventModule();
    ((VirtualEventModule) modules.get(0)).setLimit(2);
    ((VirtualEventModule) modules.get(1)).setLimit(5);

    Assertions.assertDoesNotThrow(() -> virtualEventsModuleProcessor.applyLimits(modules));
  }

  @Test
  public void applyLimitsWithHighVales() {
    List<AbstractFeaturedModule<?>> modules = getVirtualEventModule();
    ((VirtualEventModule) modules.get(0)).setLimit(15);
    ((VirtualEventModule) modules.get(1)).setLimit(5);

    Assertions.assertDoesNotThrow(() -> virtualEventsModuleProcessor.applyLimits(modules));
  }

  @Test
  public void applyLimitsWithHighAndLowVales() {
    List<AbstractFeaturedModule<?>> modules = getVirtualEventModule();
    ((VirtualEventModule) modules.get(0)).setLimit(2);
    ((VirtualEventModule) modules.get(1)).setLimit(15);

    Assertions.assertDoesNotThrow(() -> virtualEventsModuleProcessor.applyLimits(modules));
  }

  @Test
  public void applyLimitsWithNegativeLimit() {
    List<AbstractFeaturedModule<?>> modules = getVirtualEventModule();
    ((VirtualEventModule) modules.get(0)).setLimit(-2);
    ((VirtualEventModule) modules.get(1)).setLimit(15);

    Assertions.assertDoesNotThrow(() -> virtualEventsModuleProcessor.applyLimits(modules));
  }

  private SportPage virtualEventswithEventIds() {
    ArrayList<SportPageModuleDataItem> dataItems = new ArrayList<>();

    VirtualEvent virtualEvent = new VirtualEvent();
    virtualEvent.setId("65117c2dc8090c5a31a4502e");
    virtualEvent.setPageType(FeaturedRawIndex.PageType.sport);
    virtualEvent.setType("type");
    virtualEvent.setLimit(null);
    virtualEvent.setDisplayMarketType(null);
    virtualEvent.setDisplayOrder(-1);
    // virtualEvent.setTypeIds("1808,126881");

    VirtualEvent virtualEvent2 = new VirtualEvent();
    virtualEvent2.setId("65117c2dc8090c5a31a4502e");
    virtualEvent2.setPageType(FeaturedRawIndex.PageType.sport);
    virtualEvent2.setType("type");
    virtualEvent2.setLimit(3);
    virtualEvent2.setTypeIds("1811,126874");

    // add
    dataItems.add(virtualEvent);
    dataItems.add(virtualEvent2);

    SportPageModule module =
        new SportPageModule(
            SportModule.builder()
                .moduleType(ModuleType.VIRTUAL_NEXT_EVENTS)
                .sportId(39)
                .pageType(FeaturedRawIndex.PageType.sport)
                .id("virtual_next_event")
                .brand("bma")
                .title("Virtual Next Events Module")
                .build(),
            dataItems);

    return new SportPage("39", List.of(module));
  }

  List<AbstractFeaturedModule<?>> getVirtualEventModule() {
    List<AbstractFeaturedModule<?>> eventsModules = new ArrayList<>();
    VirtualEventModule virtualEvent = new VirtualEventModule();
    virtualEvent.setId("65117c2dc8090c5a31a4502e");
    virtualEvent.setPageType(FeaturedRawIndex.PageType.sport);
    virtualEvent.setLimit(null);
    virtualEvent.setDisplayMarketType(TWO_UP_MARKET);
    virtualEvent.setData(getEvents());

    VirtualEventModule virtualEvent2 = new VirtualEventModule();
    virtualEvent2.setId("65117c2dc8090c5a31a4502e");
    virtualEvent2.setPageType(FeaturedRawIndex.PageType.sport);
    virtualEvent2.setLimit(null);
    virtualEvent2.setDisplayMarketType(TWO_UP_MARKET);
    virtualEvent2.setData(getEvents());

    eventsModules.add(virtualEvent);
    eventsModules.add(virtualEvent2);
    return eventsModules;
  }

  private List<EventsModuleData> getEvents() {
    EventsModuleData eventsModuleData = new EventsModuleData();
    eventsModuleData.setMarkets(getMarkets());
    EventsModuleData eventsModuleData1 = new EventsModuleData();
    eventsModuleData1.setMarkets(getMarkets());
    eventsModuleData1.setEventIsLive(true);

    return Arrays.asList(eventsModuleData);
  }

  public static List<Event> getLiveServEvents() {
    List<Event> events = getSSEventToOutcomeForOutcome("injector_single_outcome_ids.json");
    events.get(0).setDrilldownTagNames("EVFLAG_BL");
    events.get(0).setIsLiveNowEvent(true);

    return events;
  }

  private List<Event> getLiveServFinishedEvents() {
    List<Event> events = getSSEventToOutcomeForOutcome("injector_single_outcome_ids.json");
    events.get(0).setDrilldownTagNames("EVFLAG_BL");
    events.get(0).setIsLiveNowEvent(true);
    events.get(0).setIsFinished(true);
    events.get(0).setIsStarted(true);
    return events;
  }

  private List<OutputMarket> getMarkets() {

    OutputMarket outputMarket = new OutputMarket();
    outputMarket.setId("123");
    OutputMarket outputMarket1 = new OutputMarket();
    outputMarket.setId("1234");
    return Arrays.asList(outputMarket1, outputMarket);
  }
}
