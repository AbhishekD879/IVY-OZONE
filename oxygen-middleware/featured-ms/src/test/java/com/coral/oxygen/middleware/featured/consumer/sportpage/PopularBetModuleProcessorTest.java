package com.coral.oxygen.middleware.featured.consumer.sportpage;

import static com.coral.oxygen.middleware.featured.utils.FeaturedDataUtils.getSSEventToOutcomeForOutcome;

import com.coral.oxygen.middleware.common.configuration.GsonConfiguration;
import com.coral.oxygen.middleware.common.service.SportsConfig;
import com.coral.oxygen.middleware.featured.consumer.sportpage.bets.PopularBetModuleProcessor;
import com.coral.oxygen.middleware.featured.service.PopularBetService;
import com.coral.oxygen.middleware.featured.utils.TestUtils;
import com.coral.oxygen.middleware.pojos.model.cms.featured.PopularBet;
import com.coral.oxygen.middleware.pojos.model.cms.featured.PopularBetConfig;
import com.coral.oxygen.middleware.pojos.model.cms.featured.SportModule;
import com.coral.oxygen.middleware.pojos.model.cms.featured.SportPage;
import com.coral.oxygen.middleware.pojos.model.cms.featured.SportPageModule;
import com.coral.oxygen.middleware.pojos.model.cms.featured.SportPageModuleDataItem;
import com.coral.oxygen.middleware.pojos.model.output.EventsModuleData;
import com.coral.oxygen.middleware.pojos.model.output.OutputMarket;
import com.coral.oxygen.middleware.pojos.model.output.featured.FeaturedRawIndex;
import com.coral.oxygen.middleware.pojos.model.output.featured.ModuleType;
import com.coral.oxygen.middleware.pojos.model.output.popular_bet.TrendingBetsDto;
import com.egalacoral.spark.siteserver.model.Event;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
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
    classes = {SportsConfig.class, GsonConfiguration.class, PopularBetModuleProcessor.class})
public class PopularBetModuleProcessorTest {

  @Autowired PopularBetModuleProcessor popularBetModuleProcessor;

  @MockBean PopularBetService popularBetService;

  @Test
  public void processModuleTestForException() {
    Assertions.assertDoesNotThrow(
        () ->
            popularBetModuleProcessor.processModules(
                popularBetData().getSportPageModules().get(0)));
  }

  @Test
  public void processModulesForException() {

    Mockito.doThrow(new NullPointerException())
        .when(popularBetService)
        .getTrendingBetByChannel(Mockito.any());
    Assertions.assertDoesNotThrow(
        () ->
            popularBetModuleProcessor.processModules(
                popularBetData().getSportPageModules().get(0)));
  }

  @Test
  public void processModulesForNullException() {
    Assertions.assertDoesNotThrow(
        () ->
            popularBetModuleProcessor.processModules(
                new SportPageModule(SportModule.builder().build(), null)));
  }

  @Test
  public void processModulesForLiveEvents() {

    Assertions.assertDoesNotThrow(
        () ->
            popularBetModuleProcessor.processModules(
                popularBetData().getSportPageModules().get(0)));
  }

  @Test
  public void processModulesForFinishedEvents() {

    Assertions.assertDoesNotThrow(
        () ->
            popularBetModuleProcessor.processModules(
                popularBetData().getSportPageModules().get(0)));
  }

  @Test
  public void processModulesForFinishedEventsWithConfigNull() {
    SportPageModule module = popularBetData().getSportPageModules().get(0);
    ((PopularBet) module.getPageData().get(0)).setPopularBetConfig(null);
    Assertions.assertDoesNotThrow(() -> popularBetModuleProcessor.processModules(module));
  }

  @Test
  public void processModulesForFinishedEventsWithData() {

    Mockito.doReturn(popularBetsData())
        .when(popularBetService)
        .getTrendingBetByChannel(Mockito.any());

    Assertions.assertDoesNotThrow(
        () ->
            popularBetModuleProcessor.processModules(
                popularBetData().getSportPageModules().get(0)));
  }

  private TrendingBetsDto popularBetsData() {
    return TestUtils.deserializeWithGson(
        "trendinbBetResponse/response.json", TrendingBetsDto.class);
  }

  private SportPage popularBetData() {
    ArrayList<SportPageModuleDataItem> dataItems = new ArrayList<>();

    PopularBet popularBet = new PopularBet();
    popularBet.setId("65117c2dc8090c5a31a4502e");
    popularBet.setPageType(FeaturedRawIndex.PageType.sport);
    popularBet.setType("type");
    popularBet.setPopularBetConfig(getPopularBetConfig());

    // add
    dataItems.add(popularBet);

    SportPageModule module =
        new SportPageModule(
            SportModule.builder()
                .moduleType(ModuleType.POPULAR_BETS)
                .sportId(0)
                .pageType(FeaturedRawIndex.PageType.sport)
                .id("popular_bet")
                .brand("bma")
                .title("Popular Bet Module")
                .build(),
            dataItems);

    return new SportPage("0", List.of(module));
  }

  private PopularBetConfig getPopularBetConfig() {
    PopularBetConfig popularBetConfig = new PopularBetConfig();
    popularBetConfig.setMaxSelections(5);
    popularBetConfig.setDisplayName("PopularBets");
    popularBetConfig.setEventStartsIn("24");
    popularBetConfig.setBackedInTimes("24");
    popularBetConfig.setRedirectionUrl("localhost");
    popularBetConfig.setPriceRange("24-24");
    popularBetConfig.setMostBackedIn("24");
    popularBetConfig.setEnableBackedInTimes(true);
    return popularBetConfig;
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
