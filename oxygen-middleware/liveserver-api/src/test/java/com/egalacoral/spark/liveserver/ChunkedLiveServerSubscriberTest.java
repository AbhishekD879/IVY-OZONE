package com.egalacoral.spark.liveserver;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertNotNull;
import static org.junit.Assert.assertNull;
import static org.junit.Assert.assertTrue;
import static org.mockito.Mockito.any;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.when;

import com.egalacoral.spark.liveserver.configuration.LiveServerClientBuilder;
import com.egalacoral.spark.liveserver.meta.EventMetaCachedRepoImpl;
import java.util.Iterator;
import java.util.UUID;
import java.util.stream.IntStream;
import org.junit.Before;
import org.junit.Test;
import org.mockito.Mockito;
import org.mockito.stubbing.Answer;

/**
 * @author volodymyr.masliy
 */
public class ChunkedLiveServerSubscriberTest {
  private Subscriber subscriber;
  private ChunkedNode rootChunkNode;
  private int numOfSubjectsInOneMessage;
  private LiveServerClientBuilder liveServerClientBuilder;
  private Call call;

  @Before
  public void setUp() throws Exception {
    liveServerClientBuilder = mock(LiveServerClientBuilder.class);
    call = mock(Call.class);
    when(liveServerClientBuilder.build(any()))
        .thenAnswer((Answer<LiveServerClient>) invocation -> createLiveServerClient());

    numOfSubjectsInOneMessage = 5;
    subscriber =
        new ChunkedLiveServerSubscriber(
            numOfSubjectsInOneMessage,
            liveServerClientBuilder,
            Mockito.mock(EventMetaCachedRepoImpl.class));

    rootChunkNode = ((ChunkedLiveServerSubscriber) subscriber).getRootChunkedNode();
  }

  private LiveServerClient createLiveServerClient() {
    LiveServerClient liveServerClient =
        new LiveServerClient(
            "http://localhost:8091",
            call,
            100L,
            new LiveServerListener() {
              @Override
              public void onMessage(Message message) {}

              @Override
              public void onError(Throwable e) {}
            },
            null,
            UUID.randomUUID().toString());
    return liveServerClient;
  }

  @Test
  public void testSubscriptionWorks() {
    String eventId = "1234567";
    subscriber.subscribeOnEvent(eventId, 1);
    SubscriptionSubject subject = SubscriptionSubjectFactory.onEventSubscription(eventId);

    assertTrue(rootChunkNode.isSubscribedAlready(subject));
    assertNotNull(subscriber.getPayloadItems().get(subject.messageHashKey()));
    assertEquals(1, subscriber.getPayloadItems().size());
    assertEquals(1, rootChunkNode.getChunkSize());
  }

  @Test
  public void testNewChunkIsCreatedOnceThresholdHasBeenReached() {
    generateIds(numOfSubjectsInOneMessage + 1)
        .forEach(i -> subscriber.subscribeOnEvent(String.valueOf(i), 1));

    assertEquals(numOfSubjectsInOneMessage + 1, subscriber.getPayloadItems().size());
    assertEquals(numOfSubjectsInOneMessage, rootChunkNode.getChunkSize());
    assertEquals(1, rootChunkNode.getDelegate().getChunkSize());
    assertTrue(getLiveServerClient(rootChunkNode.getDelegate()).isRunning());
  }

  @Test
  // Given chunks 1 -> 2 -> 3 -> 4,
  // test scenario when only 1 and 2 needs to be compacted, so that
  // it becomes 1 -> 3 -> 4 (without dropping 3 and 4)
  public void testChunksAreNotLostDuringCompactionWhenChunkInTheMiddleIsBeingDropped() {
    generateIds(numOfSubjectsInOneMessage * 4)
        .forEach(i -> subscriber.subscribeOnEvent(String.valueOf(i), 1));

    ChunkedLiveServerSubscriber chunkedLiveSubscriber =
        (ChunkedLiveServerSubscriber) this.subscriber;
    assertEquals(4, chunkedLiveSubscriber.getChunksStats().size());

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
    subscriber.subscribeOnEvent("5555555", 1);

    assertEquals(
        "Should be 3 chunks after compaction", 3, chunkedLiveSubscriber.getChunksStats().size());
  }

  @Test
  public void testChunkIsDeletedAndAllElementsAreCopiedToFirstChunk() {
    generateIds(numOfSubjectsInOneMessage + 1)
        .forEach(i -> subscriber.subscribeOnEvent(String.valueOf(i), 1));

    Iterator<String> iterator =
        getLiveServerClient(rootChunkNode).getPayloadItems().keySet().iterator();
    Payload payloadOfFirstChunk = getLiveServerClient(rootChunkNode).getPayload();

    for (int i = 0; i < 4; i++) {
      payloadOfFirstChunk.invalidate(iterator.next());
    }

    assertEquals("Should be one subscription in first chunk", 1, rootChunkNode.getChunkSize());

    subscriber.subscribeOnEvent("5555555", 1);

    assertEquals(3, subscriber.getPayloadItems().size());
    assertEquals(3, rootChunkNode.getChunkSize());
    assertNull("Delegate chunk should be removed", rootChunkNode.getDelegate());
  }

  @Test
  public void testChunksNotCompactedIfSumOfSizesIsBiggerThanFactorizedSize() {
    generateIds(numOfSubjectsInOneMessage + 1)
        .forEach(i -> subscriber.subscribeOnEvent(String.valueOf(i), 1));

    Iterator<String> iterator =
        getLiveServerClient(rootChunkNode).getPayloadItems().keySet().iterator();
    Payload payloadOfFirstChunk = getLiveServerClient(rootChunkNode).getPayload();

    for (int i = 0; i < 3; i++) {
      payloadOfFirstChunk.invalidate(iterator.next());
    }

    assertEquals("Should be two subscriptions in first chunk", 2, rootChunkNode.getChunkSize());

    subscriber.subscribeOnEvent("5555555", 1);

    assertEquals(4, subscriber.getPayloadItems().size());
    assertEquals(1, rootChunkNode.getDelegate().getChunkSize());
  }

  @Test
  public void testCompactionOfThreeChunksAtTheTime() {
    subscriber =
        new ChunkedLiveServerSubscriber(
            10, liveServerClientBuilder, Mockito.mock(EventMetaCachedRepoImpl.class));
    rootChunkNode = ((ChunkedLiveServerSubscriber) subscriber).getRootChunkedNode();

    generateIds(21).forEach(i -> subscriber.subscribeOnEvent(String.valueOf(i), 1));

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

    subscriber.subscribeOnEvent("5555555", 1);

    assertEquals(7, rootChunkNode.getChunkSize());
  }

  @Test
  public void testSubscriptionAlreadyExist() {
    generateIds(numOfSubjectsInOneMessage + 2)
        .forEach(i -> subscriber.subscribeOnEvent(String.valueOf(i), 1));

    generateIds(numOfSubjectsInOneMessage + 2)
        .forEach(i -> subscriber.subscribeOnEvent(String.valueOf(i), 1));

    assertEquals(7, subscriber.getPayloadItems().size());
  }

  @Test
  public void testWhenTwoChunksWithFirstIsAbleToFitSub() {
    generateIds(numOfSubjectsInOneMessage + 1)
        .forEach(i -> subscriber.subscribeOnScore(String.valueOf(i)));

    LiveServerClient firstChunkLiveServerClient = getLiveServerClient(rootChunkNode);
    firstChunkLiveServerClient
        .getPayload()
        .invalidate(firstChunkLiveServerClient.getPayloadItems().keySet().iterator().next());

    assertEquals(4, rootChunkNode.getSubscribedSubjectsMap().size());

    subscriber.subscribeOnMarket("5555555", "6666666");

    assertEquals(5, rootChunkNode.getSubscribedSubjectsMap().size());
    assertEquals(1, rootChunkNode.getDelegate().getSubscribedSubjectsMap().size());
  }

  private IntStream generateIds(int numOfIdsToGenerate) {
    return IntStream.iterate(1000000, i -> i + 1).limit(numOfIdsToGenerate);
  }

  private LiveServerClient getLiveServerClient(ChunkedNode chunkNode) {
    return ((ChunkedLiveServerSubscriber.ChunkedLiveServerNode) chunkNode).getLiveServerClient();
  }
}
