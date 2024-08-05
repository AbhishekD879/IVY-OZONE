package com.coral.oxygen.middleware.ms.liveserv.newclient.chunked;

import static org.junit.Assert.*;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.when;

import com.coral.oxygen.middleware.ms.liveserv.newclient.LiveUpdatesChannel;
import com.coral.oxygen.middleware.ms.liveserv.newclient.LiveUpdatesChannelFactory;
import com.coral.oxygen.middleware.ms.liveserv.newclient.liveserve.*;
import java.util.Iterator;
import java.util.List;
import java.util.UUID;
import java.util.stream.IntStream;
import org.junit.Before;
import org.junit.Test;
import org.mockito.Mockito;
import org.mockito.stubbing.Answer;

/**
 * @author volodymyr.masliy
 */
public class ChunkedLiveUpdatesTest {
  private ChunkedLiveUpdates subscriber;
  private ChunkedNode rootChunkNode;
  private int numOfSubjectsInOneMessage;
  private LiveServerClientBuilder liveServerClientBuilder;

  @Before
  public void setUp() throws Exception {
    liveServerClientBuilder = mock(LiveServerClientBuilder.class);
    when(liveServerClientBuilder.build())
        .thenAnswer((Answer<LiveServerClient>) invocation -> createLiveServerClient());

    numOfSubjectsInOneMessage = 5;
    subscriber = new ChunkedLiveUpdates(numOfSubjectsInOneMessage, liveServerClientBuilder);

    rootChunkNode = ((ChunkedLiveUpdates) subscriber).getRootChunkedNode();
  }

  private LiveServerClient createLiveServerClient() {
    return new LiveServerClient(
        "http://localhost:8091",
        100L,
        new LiveServerListener() {
          @Override
          public void onMessage(List<Message> message) {}

          @Override
          public void onError(Throwable e) {}
        },
        UUID.randomUUID().toString(),
        Mockito.mock(Call.class));
  }

  @Test
  public void testSubscriptionWorks() {
    String eventId = "sEVENT0001234567";
    LiveUpdatesChannel subject = LiveUpdatesChannelFactory.onEventSubscription("1234567");
    subscriber.subscribeOnItem(subject);

    assertTrue(rootChunkNode.isSubscribedAlready(subject));
    assertNotNull(subscriber.getPayloadItems().get(subject.messageHashKey()));
    assertEquals(1, subscriber.getPayloadItems().size());
    assertEquals(1, rootChunkNode.getChunkSize());
  }

  @Test
  public void testUnsubscribe() {
    LiveUpdatesChannel subject = LiveUpdatesChannelFactory.onEventSubscription("1234567");
    subscriber.subscribeOnItem(subject);

    assertEquals(1, subscriber.getPayloadItems().size());
    subscriber.unsubscribe(subject);
    assertEquals(0, subscriber.getPayloadItems().size());
  }

  @Test
  public void testNewChunkIsCreatedOnceThresholdHasBeenReached() {
    generateIds(numOfSubjectsInOneMessage + 1).forEach(i -> subscribeOnEvent(i));

    assertEquals(numOfSubjectsInOneMessage + 1, subscriber.getPayloadItems().size());
    assertEquals(numOfSubjectsInOneMessage, rootChunkNode.getChunkSize());
    assertEquals(1, rootChunkNode.getDelegate().getChunkSize());
    assertTrue(getLiveServerClient(rootChunkNode.getDelegate()).isRunning());
  }

  private void subscribeOnEvent(int eventId) {
    subscriber.subscribeOnItem(
        LiveUpdatesChannelFactory.onEventSubscription(String.valueOf(eventId)));
  }

  @Test
  // Given chunks 1 -> 2 -> 3 -> 4,
  // test scenario when only 1 and 2 needs to be compacted, so that
  // it becomes 1 -> 3 -> 4 (without dropping 3 and 4)
  public void testChunksAreNotLostDuringCompactionWhenChunkInTheMiddleIsBeingDropped() {
    generateIds(numOfSubjectsInOneMessage * 4).forEach(i -> subscribeOnEvent(i));

    ChunkedLiveUpdates chunkedLiveSubscriber = (ChunkedLiveUpdates) this.subscriber;
    assertEquals(
        4, List.class.cast(chunkedLiveSubscriber.getChunksStats().get("channelsPerChunk")).size());

    // delete all subs from root node
    LiveServerClient firstLiveServer = getLiveServerClient(rootChunkNode);
    Payload payloadOfFirstChunk = firstLiveServer.getPayload();
    firstLiveServer.getPayloadItems().keySet().forEach(payloadOfFirstChunk::invalidate);

    // delete all subs from second from root node
    LiveServerClient secondLiveServer = getLiveServerClient(rootChunkNode.getDelegate());
    Payload payloadOfSecondChunk = secondLiveServer.getPayload();
    secondLiveServer.getPayloadItems().keySet().forEach(payloadOfSecondChunk::invalidate);

    assertEquals(0, payloadOfFirstChunk.getPayloadItems().size());
    assertEquals(0, payloadOfSecondChunk.getPayloadItems().size());

    // add new sub to trigger compaction
    subscribeOnEvent(5555555);

    assertEquals(
        "Should be 3 chunks after compaction",
        3,
        List.class.cast(chunkedLiveSubscriber.getChunksStats().get("channelsPerChunk")).size());
  }

  @Test
  public void testChunkIsDeletedAndAllElementsAreCopiedToFirstChunk() {
    generateIds(numOfSubjectsInOneMessage + 1).forEach(i -> subscribeOnEvent(i));

    Iterator<String> iterator =
        getLiveServerClient(rootChunkNode).getPayloadItems().keySet().iterator();
    Payload payloadOfFirstChunk = getLiveServerClient(rootChunkNode).getPayload();

    for (int i = 0; i < 4; i++) {
      payloadOfFirstChunk.invalidate(iterator.next());
    }

    assertEquals("Should be one subscription in first chunk", 1, rootChunkNode.getChunkSize());

    subscribeOnEvent(5555555);

    assertEquals(3, subscriber.getPayloadItems().size());
    assertEquals(3, rootChunkNode.getChunkSize());
    assertNull("Delegate chunk should be removed", rootChunkNode.getDelegate());
  }

  @Test
  public void testChunksNotCompactedIfSumOfSizesIsBiggerThanFactorizedSize() {
    generateIds(numOfSubjectsInOneMessage + 1).forEach(this::subscribeOnEvent);

    Iterator<String> iterator =
        getLiveServerClient(rootChunkNode).getPayloadItems().keySet().iterator();
    Payload payloadOfFirstChunk = getLiveServerClient(rootChunkNode).getPayload();

    for (int i = 0; i < 3; i++) {
      payloadOfFirstChunk.invalidate(iterator.next());
    }

    assertEquals("Should be two subscriptions in first chunk", 2, rootChunkNode.getChunkSize());

    subscribeOnEvent(5555555);

    assertEquals(4, subscriber.getPayloadItems().size());
    assertEquals(1, rootChunkNode.getDelegate().getChunkSize());
  }

  @Test
  public void testCompactionOfThreeChunksAtTheTime() {
    subscriber = new ChunkedLiveUpdates(10, liveServerClientBuilder);
    rootChunkNode = ((ChunkedLiveUpdates) subscriber).getRootChunkedNode();

    generateIds(21).forEach(i -> subscribeOnEvent(i));

    assertNotNull(rootChunkNode.getDelegate());
    assertNotNull(rootChunkNode.getDelegate().getDelegate());
    assertNull(rootChunkNode.getDelegate().getDelegate().getDelegate());

    LiveServerClient firstChunkLiveServerClient = getLiveServerClient(rootChunkNode);
    LiveServerClient secondChunkLiveServerClient = getLiveServerClient(rootChunkNode.getDelegate());
    Iterator<String> firstChunkSubscriptions =
        firstChunkLiveServerClient.getPayloadItems().keySet().iterator();
    Iterator<String> secondChunkSubscriptions =
        secondChunkLiveServerClient.getPayloadItems().keySet().iterator();
    for (int i = 0; i < 7; i++) {
      firstChunkLiveServerClient.getPayload().invalidate(firstChunkSubscriptions.next());
      secondChunkLiveServerClient.getPayload().invalidate(secondChunkSubscriptions.next());
    }
    secondChunkLiveServerClient.getPayload().invalidate(secondChunkSubscriptions.next());

    subscribeOnEvent(5555555);

    assertEquals(7, rootChunkNode.getChunkSize());
  }

  @Test
  public void testSubscriptionAlreadyExist() {
    generateIds(numOfSubjectsInOneMessage + 2).forEach(i -> subscribeOnEvent(i));

    generateIds(numOfSubjectsInOneMessage + 2).forEach(i -> subscribeOnEvent(i));

    assertEquals(7, subscriber.getPayloadItems().size());
  }

  @Test
  public void testWhenTwoChunksWithFirstIsAbleToFitSub() {
    generateIds(numOfSubjectsInOneMessage + 1).forEach(i -> subscribeOnScore(i));

    LiveServerClient firstChunkLiveServerClient = getLiveServerClient(rootChunkNode);
    firstChunkLiveServerClient
        .getPayload()
        .invalidate(firstChunkLiveServerClient.getPayloadItems().keySet().iterator().next());

    assertEquals(4, rootChunkNode.getSubscribedSubjectsMap().size());

    //    subscriber.subscribeOnMarket("5555555", "6666666");
    subscriber.subscribeOnItem(LiveUpdatesChannelFactory.onMarketSubscription("5555555"));

    assertEquals(5, rootChunkNode.getSubscribedSubjectsMap().size());
    assertEquals(1, rootChunkNode.getDelegate().getSubscribedSubjectsMap().size());
  }

  private void subscribeOnScore(int eventId) {
    subscriber.subscribeOnItem(
        LiveUpdatesChannelFactory.onScoreSubscription(String.valueOf(eventId)));
  }

  private IntStream generateIds(int numOfIdsToGenerate) {
    return IntStream.iterate(1000000, i -> i + 1).limit(numOfIdsToGenerate);
  }

  private LiveServerClient getLiveServerClient(ChunkedNode chunkNode) {
    return ((ChunkedLiveUpdates.ChunkedLiveServerNode) chunkNode).getLiveServerClient();
  }
}
