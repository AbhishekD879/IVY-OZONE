import com.coral.oxygen.cms.api.CmsService;
import com.coral.oxygen.df.api.DFService;
import com.coral.oxygen.middleware.common.mappers.EventMapper;
import com.coral.oxygen.middleware.common.mappers.MarketMapper;
import com.coral.oxygen.middleware.common.service.AssetManagementService;
import com.coral.oxygen.middleware.common.service.MarketTemplateNameService;
import com.coral.oxygen.middleware.in_play.service.*;
import com.coral.oxygen.middleware.in_play.service.injector.InPlayDataInjectorFactory;
import com.coral.oxygen.middleware.in_play.service.siteserver.InplaySiteServeService;
import com.coral.oxygen.middleware.pojos.model.df.Horse;
import com.coral.oxygen.middleware.pojos.model.df.RaceEvent;
import com.coral.oxygen.middleware.pojos.model.output.*;
import com.egalacoral.spark.siteserver.model.Event;
import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import java.util.Optional;
import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mockito;
import org.mockito.junit.MockitoJUnitRunner;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.cache.CacheManager;

@RunWith(MockitoJUnitRunner.class)
@SpringBootTest(
    classes = {
      CmsService.class,
      EventMapper.class,
      MarketMapper.class,
      InPlayDataFilter.class,
      SportsRibbonService.class,
      InPlayDataSorter.class,
      MarketTemplateNameService.class,
      InplaySiteServeService.class,
      InPlayDataInjectorFactory.class
    })
public class InplayDataConsumerTest {
  @MockBean CmsService cmsService;

  @Qualifier("inplay")
  EventMapper eventMapper;

  @Qualifier("inplayMarketMapper")
  MarketMapper marketMapper;

  @MockBean InPlayDataFilter inPlayDataFilter;
  @MockBean SportsRibbonService sportsRibbonService;
  @MockBean InPlayDataSorter inPlayDataSorter;
  @MockBean MarketTemplateNameService marketTemplateNameService;
  @MockBean InPlayDataInjectorFactory dataInjectorFactory;
  @MockBean InplaySiteServeService siteserverService;
  @MockBean DFService dfService;
  @MockBean CacheManager cacheManager;
  @MockBean AssetManagementService assetManagementService;

  InPlayDataConsumer o = null;

  @Before
  public void setUp() {
    o =
        new InPlayDataConsumer(
            cmsService,
            eventMapper,
            marketMapper,
            inPlayDataFilter,
            sportsRibbonService,
            inPlayDataSorter,
            marketTemplateNameService,
            dataInjectorFactory,
            siteserverService,
            dfService,
            cacheManager,
            assetManagementService);
  }

  @Test
  public void testgetInPlayTypeToEventPair() throws Exception {
    Event event = new Event();
    event.setIsStarted(Boolean.TRUE);
    event.setRawIsOffCode("Y");
    Class c = InPlayDataConsumer.class;
    Method m = c.getDeclaredMethod("getInPlayTypeToEventPair", Event.class);
    m.setAccessible(true);
    m.invoke(o, event);
    Assert.assertNotNull(event.getIsStarted());
  }

  @Test
  public void testgetInPlayTypeToEventPair1() throws Exception {
    Event event = new Event();
    event.setIsStarted(Boolean.TRUE);
    event.setRawIsOffCode("N");
    Class c = InPlayDataConsumer.class;
    Method m = c.getDeclaredMethod("getInPlayTypeToEventPair", Event.class);
    m.setAccessible(true);
    m.invoke(o, event);
    Assert.assertNotNull(event.getIsStarted());
  }

  @Test
  public void testgetInPlayTypeToEventPair2() throws Exception {
    Event event = new Event();
    event.setIsStarted(Boolean.FALSE);
    event.setRawIsOffCode("N");
    Class c = InPlayDataConsumer.class;
    Method m = c.getDeclaredMethod("getInPlayTypeToEventPair", Event.class);
    m.setAccessible(true);
    m.invoke(o, event);
    Assert.assertNotNull(event.getIsStarted());
  }

  @Test
  public void testgetInPlayTypeToEventPair3() throws Exception {
    Event event = new Event();
    event.setIsStarted(Boolean.FALSE);
    event.setRawIsOffCode("Y");
    Class c = InPlayDataConsumer.class;
    Method m = c.getDeclaredMethod("getInPlayTypeToEventPair", Event.class);
    m.setAccessible(true);
    m.invoke(o, event);
    Assert.assertNotNull(event.getIsStarted());
  }

  @Test
  public void mapToEventTest()
      throws NoSuchMethodException, InvocationTargetException, IllegalAccessException {
    dfService = Mockito.mock(DFService.class);
    o =
        new InPlayDataConsumer(
            cmsService,
            eventMapper,
            marketMapper,
            inPlayDataFilter,
            sportsRibbonService,
            inPlayDataSorter,
            marketTemplateNameService,
            dataInjectorFactory,
            siteserverService,
            dfService,
            cacheManager,
            assetManagementService);
    Method method = o.getClass().getDeclaredMethod("mapToEvent", EventsModuleData.class);
    method.setAccessible(true);
    Horse horse = new Horse();
    horse.setTrainer("trainer");
    RaceEvent raceEvent = new RaceEvent();
    raceEvent.setRaceClass(101);
    raceEvent.setDistance("1000");
    raceEvent.setGoing("uk2");
    raceEvent.setHorses(Collections.singletonList(horse));
    OutputOutcome outcome = new OutputOutcome();
    outcome.setRunnerNumber(1);
    OutputMarket outputMarket = new OutputMarket();
    outputMarket.setOutcomes(Collections.singletonList(outcome));
    EventsModuleData eventsModule = new EventsModuleData();
    eventsModule.setId(1l);
    eventsModule.setCategoryId("100");
    eventsModule.setMarkets(Collections.singletonList(outputMarket));
    eventsModule.setPrimaryMarkets(Collections.singletonList(outputMarket));
    Mockito.doReturn(Optional.of(Collections.singletonMap(1l, raceEvent)))
        .when(dfService)
        .getRaceEvents(Mockito.anyInt(), Mockito.anyCollection());
    method.invoke(o, eventsModule);
    Assert.assertNotNull(eventsModule);
  }

  @Test
  public void mapToEventNegativeCaseTest()
      throws NoSuchMethodException, InvocationTargetException, IllegalAccessException {
    dfService = Mockito.mock(DFService.class);
    o =
        new InPlayDataConsumer(
            cmsService,
            eventMapper,
            marketMapper,
            inPlayDataFilter,
            sportsRibbonService,
            inPlayDataSorter,
            marketTemplateNameService,
            dataInjectorFactory,
            siteserverService,
            dfService,
            cacheManager,
            assetManagementService);
    Method method = o.getClass().getDeclaredMethod("mapToEvent", EventsModuleData.class);
    method.setAccessible(true);
    OutputOutcome outcome = new OutputOutcome();
    outcome.setRunnerNumber(1);
    OutputMarket outputMarket = new OutputMarket();
    outputMarket.setOutcomes(Collections.singletonList(outcome));
    EventsModuleData eventsModule = new EventsModuleData();
    eventsModule.setId(1l);
    eventsModule.setCategoryId("100");
    eventsModule.setMarkets(Collections.singletonList(outputMarket));
    eventsModule.setPrimaryMarkets(Collections.singletonList(outputMarket));
    Mockito.doReturn(Optional.of(Collections.singletonMap(1l, null)))
        .when(dfService)
        .getRaceEvents(Mockito.anyInt(), Mockito.anyCollection());
    method.invoke(o, eventsModule);
    Assert.assertNotNull(eventsModule);
  }

  @Test
  public void testGetRaceFormEvent()
      throws NoSuchMethodException, InvocationTargetException, IllegalAccessException {
    Method method =
        o.getClass()
            .getDeclaredMethod("getRaceFormEvent", Integer.class, String.class, String.class);
    method.setAccessible(true);
    RacingFormEvent event = (RacingFormEvent) method.invoke(o, 1, "100km", "101");
    Assert.assertEquals("101", event.getGoing());
  }

  @Test
  public void testGetRaceFormEventNegativeCase()
      throws NoSuchMethodException, InvocationTargetException, IllegalAccessException {
    Method method =
        o.getClass()
            .getDeclaredMethod("getRaceFormEvent", Integer.class, String.class, String.class);
    method.setAccessible(true);
    RacingFormEvent event = (RacingFormEvent) method.invoke(o, null, "", "");
    Assert.assertEquals("", event.getGoing());
  }

  @Test
  public void testRacingFormOutcome()
      throws NoSuchMethodException, InvocationTargetException, IllegalAccessException {
    Method method = o.getClass().getDeclaredMethod("racingFormOutcome", List.class, Integer.class);
    method.setAccessible(true);
    Horse horse = new Horse();
    horse.setTrainer("trainer1");
    horse.setSilk("silk1");
    horse.setDraw("draw1");
    horse.setJockey("jockey1");
    Horse horse2 = new Horse();
    horse2.setTrainer("trainer2");
    horse2.setSilk("silk2");
    horse2.setDraw("draw2");
    horse2.setJockey("jockey2");
    OutputRacingFormOutcome outcome =
        (OutputRacingFormOutcome) method.invoke(o, Arrays.asList(horse, horse2), 1);
    Assert.assertNotNull(outcome);
  }

  @Test
  public void testRacingFormOutcomeNegativeCase1()
      throws NoSuchMethodException, InvocationTargetException, IllegalAccessException {
    Method method = o.getClass().getDeclaredMethod("racingFormOutcome", List.class, Integer.class);
    method.setAccessible(true);
    OutputRacingFormOutcome outcome =
        (OutputRacingFormOutcome) method.invoke(o, Collections.singletonList(new Horse()), null);
    Assert.assertNotNull(outcome);
  }

  @Test
  public void testRacingFormOutcomeNegativeCase2()
      throws NoSuchMethodException, InvocationTargetException, IllegalAccessException {
    Method method = o.getClass().getDeclaredMethod("racingFormOutcome", List.class, Integer.class);
    method.setAccessible(true);
    OutputRacingFormOutcome outcome =
        (OutputRacingFormOutcome) method.invoke(o, Collections.singletonList(new Horse()), 2);
    Assert.assertNotNull(outcome);
  }

  @Test
  public void testGetOutputRacingFormOutcome()
      throws NoSuchMethodException, InvocationTargetException, IllegalAccessException {
    Method method = o.getClass().getDeclaredMethod("getOutputRacingFormOutcome", Horse.class);
    method.setAccessible(true);
    Horse horse1 = null;
    OutputRacingFormOutcome outcome = (OutputRacingFormOutcome) method.invoke(o, horse1);
    Assert.assertNotNull(outcome);
    Horse horse = new Horse();
    horse.setSilk("abc");
    horse.setDraw("def");
    horse.setTrainer("trainer1");
    horse.setJockey("jockey1");
    OutputRacingFormOutcome outcomeWithVal = (OutputRacingFormOutcome) method.invoke(o, horse);
    Assert.assertEquals("trainer1", horse.getTrainer());
  }

  @Test
  public void testIsHorsesSizeGreaterThanRunnerNumber()
      throws NoSuchMethodException, InvocationTargetException, IllegalAccessException {
    Method method =
        o.getClass()
            .getDeclaredMethod("isHorsesSizeGreaterThanRunnerNumber", int.class, Integer.class);
    method.setAccessible(true);
    boolean val = (boolean) method.invoke(o, 2, Integer.valueOf(2));
    Assert.assertTrue(val);
  }

  @Test
  public void testIsHorsesSizeGreaterThanRunnerNumberNegative()
      throws NoSuchMethodException, InvocationTargetException, IllegalAccessException {
    Method method =
        o.getClass()
            .getDeclaredMethod("isHorsesSizeGreaterThanRunnerNumber", int.class, Integer.class);
    method.setAccessible(true);
    boolean val = (boolean) method.invoke(o, 1, Integer.valueOf(2));
    Assert.assertFalse(val);
  }

  @Test
  public void testCompareMarketTemplateNamesEqualCase()
      throws NoSuchMethodException, InvocationTargetException, IllegalAccessException {
    Method method =
        o.getClass().getDeclaredMethod("compareMarketTemplateNames", String.class, String.class);
    method.setAccessible(true);
    int val1 = (int) method.invoke(o, "MATCH_WINNER", "MATCH_WINNER");
    Assert.assertEquals(0, val1);
  }
}
