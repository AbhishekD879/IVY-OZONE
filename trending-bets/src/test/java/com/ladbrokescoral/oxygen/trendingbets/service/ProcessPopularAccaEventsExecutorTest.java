package com.ladbrokescoral.oxygen.trendingbets.service;

import static org.mockito.Mockito.doThrow;
import static org.mockito.Mockito.mock;

import com.ladbrokescoral.oxygen.trendingbets.context.PopularAccaContext;
import com.ladbrokescoral.oxygen.trendingbets.model.OutputMarket;
import com.ladbrokescoral.oxygen.trendingbets.model.OutputOutcome;
import com.ladbrokescoral.oxygen.trendingbets.model.TrendingEvent;
import com.ladbrokescoral.oxygen.trendingbets.model.TrendingPosition;
import java.lang.reflect.Constructor;
import java.util.*;
import java.util.concurrent.ArrayBlockingQueue;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.TimeUnit;
import lombok.extern.slf4j.Slf4j;
import org.jetbrains.annotations.NotNull;
import org.junit.Assert;
import org.junit.jupiter.api.*;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.springframework.test.context.junit.jupiter.SpringExtension;
import org.springframework.test.util.ReflectionTestUtils;

@Slf4j
@ExtendWith(SpringExtension.class)
@TestMethodOrder(MethodOrderer.OrderAnnotation.class)
class ProcessPopularAccaEventsExecutorTest {

  @InjectMocks PopularAccaExecutor executor;

  PopularAccaContext popularAccaContext;

  @BeforeEach
  public void init() throws Exception {

    Constructor<?> constructor = PopularAccaContext.class.getDeclaredConstructor();
    constructor.setAccessible(true);
    popularAccaContext = (PopularAccaContext) constructor.newInstance();

    executor =
        new PopularAccaExecutor(
            new String[] {"MKTFLAG_SP"}, new String[] {"EVTFLAG_SP"}, new String[] {"Outright"});
    executor.runUploadWorkers();
    PopularAccaContext.getEventAccas().clear();
    PopularAccaContext.getSelectionAccas().clear();
    PopularAccaContext.getLeagueAccas().clear();
  }

  @Test
  void addItem() throws InterruptedException {
    CountDownLatch latch = new CountDownLatch(1);
    PopularAccaContext.addItemsToQueue(
        "24_14", createTwoPostions("selection5", "eventId4", 230, 1, 10));
    PopularAccaContext.addItemsToQueue(
        "24_14", createTwoPostions("selection5", "eventId4", 231, 1, 10));
    PopularAccaContext.addItemsToQueue(
        "24_14", createTwoPostions("selection5", "eventId4", 232, 1, 10));
    PopularAccaContext.addItemsToQueue(
        "24_24", createTwoPostions("selection6", "eventId4", 240, 1, 10));
    PopularAccaContext.addItemsToQueue(
        "24_24", createTwoPostions("selection6", "eventId4", 241, 1, 1));
    PopularAccaContext.addItemsToQueue(
        "24_24", createTwoPostions("selection6", "eventId4", 242, 0, 1));
    PopularAccaContext.addItemsToQueue(
        "24_24", createTwoPostions("selection6", "eventId4", 240, 1, 0));
    PopularAccaContext.addItemsToQueue(
        "24_24", createTwoPostions("selection11", "eventId11", 240, 1, 0));
    PopularAccaContext.addItemsToQueue(
        "24_25", createTwoPostions("selection5", "eventId4", 300, 1, 1));

    latch.await(10, TimeUnit.SECONDS);
    Assert.assertNotNull(PopularAccaContext.getSelectionAccas().get("selection5"));
    Assert.assertNotNull(PopularAccaContext.getSelectionAccas().get("selection1"));
    Assert.assertEquals(0, PopularAccaContext.getUploadPendingItems().size());
  }

  @Test
  void addItemDrillDownTagNames() throws InterruptedException {
    CountDownLatch latch = new CountDownLatch(1);

    TreeSet<TrendingPosition> validTemplates =
        createTwoPostions("selection1", "eventId1", 260, 1, 10);
    validTemplates.forEach(
        position -> {
          position.getEvent().setDrilldownTagNames("EVTFLAG_SP");
          position.getEvent().getMarkets().get(0).setDrilldownTagNames("MKTFLAG_SP");
        });
    PopularAccaContext.addItemsToQueue("24_21", validTemplates);

    TreeSet<TrendingPosition> invalidMarkettemplate =
        createTwoPostions("selection2", "eventId2", 261, 1, 10);
    invalidMarkettemplate.forEach(
        position -> {
          position.getEvent().setDrilldownTagNames("EVTFLAG_SP");
          position.getEvent().getMarkets().get(0).setDrilldownTagNames("invalid");
        });
    PopularAccaContext.addItemsToQueue("24_22", invalidMarkettemplate);

    TreeSet<TrendingPosition> invalidEventTemplate =
        createTwoPostions("selection3", "eventId3", 262, 1, 10);
    invalidEventTemplate.forEach(
        position -> {
          position.getEvent().setDrilldownTagNames("invalid");
          position.getEvent().getMarkets().get(0).setDrilldownTagNames("MKTFLAG_SP");
        });
    PopularAccaContext.addItemsToQueue("24_23", invalidEventTemplate);

    TreeSet<TrendingPosition> invalidtemplates =
        createTwoPostions("selection4", "eventId4", 263, 1, 10);
    invalidEventTemplate.forEach(
        position -> {
          position.getEvent().setDrilldownTagNames("invalid");
          position.getEvent().getMarkets().get(0).setDrilldownTagNames("invalid");
        });
    PopularAccaContext.addItemsToQueue("24_24", invalidtemplates);

    latch.await(10, TimeUnit.SECONDS);

    Assert.assertEquals(0, PopularAccaContext.getUploadPendingItems().size());
  }

  @Test
  void addItemMinMaxAcca() throws InterruptedException {
    CountDownLatch latch = new CountDownLatch(1);
    TreeSet<TrendingPosition> postions = new TreeSet<>();

    postions.add(
        createPostion(231, getTrendingEvent("selection5", "eventId4", "typeId1", 1, 0), 231));
    postions.add(
        createPostion(232, getTrendingEvent("selection6", "eventId5", "typeId1", 1, 1), 232));
    postions.add(
        createPostion(233, getTrendingEvent("selection7", "eventId6", "typeId1", 0, 0), 233));
    postions.add(
        createPostion(234, getTrendingEvent("selection8", "eventId7", "typeId1", 1, 10), 234));
    postions.add(
        createPostion(235, getTrendingEvent("selection8", "eventId8", "typeId1", 0, 1), 235));
    PopularAccaContext.addItemsToQueue("24_14", postions);

    latch.await(10, TimeUnit.SECONDS);
    Assert.assertEquals(3, PopularAccaContext.getSelectionAccas().size());
  }

  @Test
  void addItemWithNoOutRights() throws InterruptedException {
    CountDownLatch latch = new CountDownLatch(1);

    TreeSet<TrendingPosition> ourightmarket =
        createTwoPostions("selection1", "eventId1", 261, 1, 25);
    ourightmarket.forEach(
        position -> {
          position.getEvent().getMarkets().get(0).setTemplateMarketName("Outright");
        });
    PopularAccaContext.addItemsToQueue("24_23", ourightmarket);

    TreeSet<TrendingPosition> normalmarket =
        createTwoPostions("selection2", "eventId2", 262, 1, 25);
    ourightmarket.forEach(
        position -> {
          position.getEvent().getMarkets().get(0).setTemplateMarketName("Outright1");
        });
    PopularAccaContext.addItemsToQueue("24_24", normalmarket);

    latch.await(10, TimeUnit.SECONDS);
    Assert.assertEquals(0, PopularAccaContext.getUploadPendingItems().size());
  }

  @Test
  void addItemWithOutMarketsWhichDonotFormAcca() throws InterruptedException {
    CountDownLatch latch = new CountDownLatch(1);
    PopularAccaContext.addItemsToQueue(
        "24_14", createTwoPostions("selection5", "eventId4", 230, 1, 1));
    PopularAccaContext.addItemsToQueue(
        "24_14", createTwoPostions("selection5", "eventId4", 231, 1, 1));
    PopularAccaContext.addItemsToQueue(
        "24_14", createTwoPostions("selection5", "eventId4", 232, 1, 1));
    PopularAccaContext.addItemsToQueue(
        "24_24", createTwoPostions("selection6", "eventId4", 240, 1, 1));

    TreeSet<TrendingPosition> postions = createTwoPostions("selection5", "eventId4", 260, 1, 1);
    postions.forEach(position -> position.getEvent().setDrilldownTagNames("EVTFLAG_SP"));
    PopularAccaContext.addItemsToQueue("24_23", postions);
    TreeSet<TrendingPosition> outrightPositions =
        createTwoPostions("selection5", "eventId4", 300, 1, 1);
    outrightPositions.forEach(
        position -> position.getEvent().getMarkets().get(0).setTemplateMarketName("Outright"));
    PopularAccaContext.addItemsToQueue("24_25", outrightPositions);

    latch.await(10, TimeUnit.SECONDS);
    Assert.assertEquals(0, PopularAccaContext.getSelectionAccas().size());
    Assert.assertEquals(0, PopularAccaContext.getEventAccas().size());
    Assert.assertEquals(0, PopularAccaContext.getLeagueAccas().size());

    Assert.assertNull(PopularAccaContext.getSelectionAccas().get("selection5"));
    Assert.assertNull(PopularAccaContext.getSelectionAccas().get("selection1"));
    Assert.assertEquals(0, PopularAccaContext.getUploadPendingItems().size());
  }

  @Test
  void testPurgeAcca() {
    TrendingPosition position1 = createPostion(231, getTrendingEvent("s1", "e1", "t1", 1, 0), 231);
    TrendingPosition position2 = createPostion(231, getTrendingEvent("s2", "e1", "t1", 1, 0), 231);
    Set<TrendingPosition> positions = new HashSet<>();
    positions.add(position1);
    positions.add(position2);
    Map<String, Set<TrendingPosition>> accas = new HashMap<>();
    accas.put("t1", positions);
    PopularAccaContext.purgeAcca(accas, "t1", position1);
    PopularAccaContext.purgeAcca(accas, "t1", position2);
    Assert.assertEquals(0, accas.size());
  }

  public TreeSet<TrendingPosition> createTwoPostions(
      String selection, String eventId, int nbets, int minAcca, int maxAcca) {
    TreeSet<TrendingPosition> postions = new TreeSet<>();
    postions.add(
        createPostion(
            nbets, getTrendingEvent(selection, eventId, "typeId1", minAcca, maxAcca), nbets));
    postions.add(
        createPostion(1, getTrendingEvent("selection1", "event1", "typeId1", minAcca, maxAcca), 2));

    return postions;
  }

  @Test
  void testInterruptedException() throws InterruptedException {

    ArrayBlockingQueue uploadQueue = mock(ArrayBlockingQueue.class);
    ReflectionTestUtils.setField(popularAccaContext, "uploadPendingQueue", uploadQueue);
    doThrow(new InterruptedException()).when(uploadQueue).put("interruptException");
    PopularAccaContext.addItemsToQueue(
        "interruptException", createTwoPostions("selection24", "eventId24", 230, 1, 1));
    Assert.assertEquals(0, PopularAccaContext.getSelectionAccas().size());
  }

  private TrendingPosition createPostion(int nbets, TrendingEvent event, int rank) {

    TrendingPosition position = new TrendingPosition();
    position.setEvent(event);
    position.setNBets(nbets);
    position.setRank(rank);
    position.setPreviousRank(rank);
    return position;
  }

  @NotNull
  private TrendingEvent getTrendingEvent(
      String selectionId, String eventId, String typeId, int minAcc, int maxAcc) {
    TrendingEvent event = new TrendingEvent();
    event.setLiveServChannels(selectionId);
    event.setSelectionId(selectionId);
    event.setId(eventId);
    event.setTypeId(typeId);

    OutputOutcome outcome = new OutputOutcome();
    outcome.setId(selectionId);
    outcome.setLiveServChannels(selectionId);
    OutputMarket market = new OutputMarket();
    market.setId("");
    market.setLiveServChannels(selectionId);
    market.setOutcomes(List.of(outcome));
    market.setMinAccumulators(minAcc);
    market.setMaxAccumulators(maxAcc);
    event.setMarkets(List.of(market));
    return event;
  }

  @AfterEach
  public void shutdown() {
    PopularAccaContext.getEventAccas().clear();
    PopularAccaContext.getSelectionAccas().clear();
    PopularAccaContext.getLeagueAccas().clear();
    executor.shutdown();
  }
}
