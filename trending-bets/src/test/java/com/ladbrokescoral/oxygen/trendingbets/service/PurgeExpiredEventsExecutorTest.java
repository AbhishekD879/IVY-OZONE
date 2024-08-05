package com.ladbrokescoral.oxygen.trendingbets.service;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.*;

import com.ladbrokescoral.oxygen.trendingbets.context.TrendingBetsContext;
import com.ladbrokescoral.oxygen.trendingbets.model.OutputMarket;
import com.ladbrokescoral.oxygen.trendingbets.model.OutputOutcome;
import com.ladbrokescoral.oxygen.trendingbets.model.TrendingEvent;
import java.lang.reflect.Constructor;
import java.util.ArrayList;
import java.util.List;
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
class PurgeExpiredEventsExecutorTest {

  @InjectMocks PurgeExpiredEventsExecutor executor;

  private TrendingBetsContext trendingBetsContext;

  @BeforeEach
  public void init() throws Exception {

    Constructor<?> constructor =
        TrendingBetsContext.class.getDeclaredConstructor(
            Integer.class, Integer.class, Integer.class);
    constructor.setAccessible(true);
    trendingBetsContext = (TrendingBetsContext) constructor.newInstance(1, 7, 2);
    executor = new PurgeExpiredEventsExecutor(2);
    executor.runUploadWorkers();
  }

  @Test
  void addItem() throws InterruptedException {
    CountDownLatch latch = new CountDownLatch(1);
    TrendingBetsContext.getPersonalizedSelections()
        .put("12345608", prepareTrendingEventList("12345608"));
    latch.await(100, TimeUnit.MILLISECONDS);
    Assert.assertEquals(0, TrendingBetsContext.getUploadPendingItems().size());
    Assert.assertEquals(1, TrendingBetsContext.getPersonalizedSelections().size());
  }

  @Test
  void addItemWithExceedMaxSize() throws InterruptedException {
    CountDownLatch latch = new CountDownLatch(1);

    TrendingBetsContext.getPersonalizedSelections()
        .put("12345605", prepareTrendingEventList("12345605"));
    TrendingBetsContext.getPersonalizedSelections()
        .computeIfAbsent("12345605", (key) -> new ArrayList<>());
    TrendingBetsContext.getPersonalizedSelections()
        .put("12345706", prepareTrendingEventList("12345706"));
    TrendingBetsContext.getPersonalizedSelections().entrySet();

    latch.await(5, TimeUnit.SECONDS);
    Assert.assertEquals(0, TrendingBetsContext.getUploadPendingItems().size());
    Assert.assertEquals(1, TrendingBetsContext.getPersonalizedSelections().size());
  }

  @Test
  void addItemForQueuMonitor() throws InterruptedException {
    CountDownLatch latch = new CountDownLatch(1);

    for (int i = 0; i < 10; i++) {
      String selectionId = String.valueOf(i);
      TrendingBetsContext.getPersonalizedSelections()
          .put(selectionId, prepareTrendingEventList(selectionId));
    }

    latch.await(5, TimeUnit.SECONDS);
    Assert.assertEquals(0, TrendingBetsContext.getUploadPendingItems().size());
    Assert.assertEquals(1, TrendingBetsContext.getPersonalizedSelections().size());
  }

  @Test
  void addItemWithExpiry() throws InterruptedException {

    CountDownLatch latch = new CountDownLatch(1);
    TrendingBetsContext.getPersonalizedSelections()
        .put("12345603", prepareTrendingEventList("12345603"));

    latch.await(8, TimeUnit.SECONDS);
    Assert.assertEquals(0, TrendingBetsContext.getUploadPendingItems().size());
    Assert.assertEquals(0, TrendingBetsContext.getPersonalizedSelections().size());
  }

  @Test
  void addItemWithException() throws InterruptedException {
    CountDownLatch latch = new CountDownLatch(1);

    List<TrendingEvent> events = prepareTrendingEventList("12345601");
    events.get(0).setMarkets(null);
    TrendingBetsContext.getPersonalizedSelections().put("12345601", events);
    TrendingBetsContext.getPersonalizedSelections()
        .put("12345702", prepareTrendingEventList("12345702"));

    latch.await(2, TimeUnit.SECONDS);

    Assert.assertEquals(1, TrendingBetsContext.getPersonalizedSelections().size());
  }

  @Test
  void addItemWithOutException() throws InterruptedException {
    CountDownLatch latch = new CountDownLatch(1);

    TrendingBetsContext.getPersonalizedSelections()
        .put("12345602", prepareTrendingEventList("12345602"));
    TrendingBetsContext.getPersonalizedSelections()
        .put("12345703", prepareTrendingEventList("12345703"));

    latch.await(4, TimeUnit.SECONDS);

    Assert.assertEquals(1, TrendingBetsContext.getPersonalizedSelections().size());
  }

  @Test
  void testInterruptedException() throws InterruptedException {
    ArrayBlockingQueue uploadQueue = mock(ArrayBlockingQueue.class);
    ReflectionTestUtils.setField(trendingBetsContext, "uploadPendingQueue", uploadQueue);
    doThrow(new InterruptedException()).when(uploadQueue).put(any());
    CountDownLatch latch = new CountDownLatch(1);

    TrendingBetsContext.getPersonalizedSelections()
        .put("12345601", prepareTrendingEventList("12345601"));
    TrendingBetsContext.getPersonalizedSelections()
        .put("12345702", prepareTrendingEventList("12345702"));

    latch.await(2, TimeUnit.SECONDS);

    Assert.assertEquals(1, TrendingBetsContext.getPersonalizedSelections().size());
  }

  public List<TrendingEvent> prepareTrendingEventList(String selectionId) {

    final TrendingEvent event = getTrendingEvent(selectionId);
    return List.of(event);
  }

  @NotNull
  private static TrendingEvent getTrendingEvent(String selectionId) {
    TrendingEvent event = new TrendingEvent();
    event.setLiveServChannels(selectionId);
    event.setSelectionId(selectionId);
    OutputOutcome outcome = new OutputOutcome();
    outcome.setId(selectionId);
    outcome.setLiveServChannels(selectionId);
    OutputMarket market = new OutputMarket();
    market.setId("");
    market.setLiveServChannels(selectionId);
    market.setOutcomes(List.of(outcome));
    event.setMarkets(List.of(market));
    return event;
  }

  @AfterEach
  public void shutdown() {
    executor.shutdown();
    TrendingBetsContext.getPersonalizedSelections().clear();
  }
}
