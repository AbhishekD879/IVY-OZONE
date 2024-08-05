package com.egalacoral.spark.liveserver;

import com.egalacoral.spark.liveserver.configuration.LiveServerClientBuilder;
import com.egalacoral.spark.liveserver.meta.EventMetaInfoCachedRepository;
import java.math.BigInteger;
import java.util.ArrayList;
import java.util.Collection;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

/**
 * Subscribes on subjects with breaking them in chunks of predefined size if needed;
 *
 * <p>If chunk's size has been reached, new chunk will be created dynamically. Vice versa, subjects
 * will be moved to one chunk if they fit it
 *
 * @author volodymyr.masliy
 */
@Slf4j
@Component
public class ChunkedLiveServerSubscriber implements Subscriber {
  /**
   * Given two chunks, if sum of their subjects is less then FILL_FACTOR *
   * numOfSubjectsInOneMessage, then these chunks can be compacted. See #{@link
   * ChunkedLiveServerNode#compact()}
   */
  private static final double FILL_FACTOR = 0.75;

  private final int numOfSubjectsInOneMessage;
  private final int maxSizeOfChunkAfterCompaction;
  private final EventMetaInfoCachedRepository eventMetaInfoRepository;
  private ChunkedNode rootNode;
  private LiveServerClientBuilder liveServerClientBuilder;

  @Autowired
  public ChunkedLiveServerSubscriber(
      @Value("${liveServer.subscription.limitPerClient:3200}") int numOfSubjectsInOneMessage,
      LiveServerClientBuilder liveServerClientBuilder,
      EventMetaInfoCachedRepository eventMetaInfoRepository) {
    this.numOfSubjectsInOneMessage = numOfSubjectsInOneMessage;
    this.maxSizeOfChunkAfterCompaction = (int) (FILL_FACTOR * numOfSubjectsInOneMessage);
    this.liveServerClientBuilder = liveServerClientBuilder;
    this.rootNode =
        new ChunkedLiveServerNode(liveServerClientBuilder.build(eventMetaInfoRepository));
    this.eventMetaInfoRepository = eventMetaInfoRepository;
  }

  @Override
  public void subscribeOnClock(String eventId) {
    subscribeOnItem(SubscriptionSubjectFactory.onClockSubscription(eventId));
  }

  @Override
  public void subscribeOnEvent(String eventId, int categoryId) {
    subscribeOnItem(SubscriptionSubjectFactory.onEventSubscription(eventId));
    eventMetaInfoRepository.putByEventId(new BigInteger(eventId), categoryId);
  }

  @Override
  public void subscribeOnMarket(String marketId, String eventId) {
    subscribeOnItem(SubscriptionSubjectFactory.onMarketSubscription(marketId));
    eventMetaInfoRepository.putByMarketId(new BigInteger(marketId), new BigInteger(eventId));
  }

  @Override
  public void subscribeOnScore(String eventId) {
    subscribeOnItem(SubscriptionSubjectFactory.onScoreSubscription(eventId));
  }

  @Override
  public void subscribeOnSelection(String selectionId, String eventId) {
    subscribeOnItem(SubscriptionSubjectFactory.onSelectionSubscription(selectionId));
    eventMetaInfoRepository.putBySelectionId(new BigInteger(selectionId), new BigInteger(eventId));
  }

  private void subscribeOnItem(SubscriptionSubject subject) {
    log.debug("Subscribe to item {}", subject);
    rootNode.subscribe(subject);
  }

  public List<Integer> getChunksStats() {
    List<Integer> stats = new ArrayList<>();
    ChunkedNode node = rootNode;
    while (node != null) {
      stats.add(node.getChunkSize());
      node = node.getDelegate();
    }
    return stats;
  }

  @Override
  public Map<String, SubscriptionSubject> getPayloadItems() {
    Map<String, SubscriptionSubject> subs = new HashMap<>();
    ChunkedNode node = rootNode;
    while (node != null) {
      subs.putAll(node.getSubscribedSubjectsMap());
      node = node.getDelegate();
    }
    return subs;
  }

  ChunkedNode getRootChunkedNode() {
    return rootNode;
  }

  /**
   * Wraps #{@link LiveServerClient} to control maximum number of subscription per client and
   * delegate subscription another #{@link ChunkedNode} if threshold has been reached.
   *
   * <p>Will try to reduce number of parallel #{@link LiveServerClient} based on #{@link
   * ChunkedLiveServerNode#canBeCompacted}
   */
  class ChunkedLiveServerNode implements ChunkedNode {
    private final LiveServerClient liveServerClient;
    private ChunkedNode delegate;

    public ChunkedLiveServerNode(LiveServerClient liveServerClient) {
      this.liveServerClient = liveServerClient;
    }

    @Override
    public int getChunkSize() {
      return liveServerClient.getPayloadItems().size();
    }

    @Override
    public boolean isMaxChunkSizeReached() {
      return getChunkSize() >= numOfSubjectsInOneMessage;
    }

    @Override
    public void subscribe(SubscriptionSubject subject) {
      if (isSubscribedAlready(subject)) {
        log.debug("Subscription already exist: {}", subject);
        return;
      }

      if (!isMaxChunkSizeReached()) {
        doSubscribe(subject);
        compact();
      } else {
        if (delegate == null) {
          LiveServerClient newLiveServerClient =
              liveServerClientBuilder.build(eventMetaInfoRepository);
          log.info(
              "Max chunk size has been reached for LiveServerClient <{}>. Creating LiveServerClient <{}>. Was adding {}",
              liveServerClient.getId(),
              newLiveServerClient.getId(),
              subject);
          delegate = new ChunkedLiveServerNode(newLiveServerClient);
        }
        delegate.subscribe(subject);
      }

      if (!liveServerClient.isRunning()) {
        liveServerClient.connect();
      }
    }

    private void doSubscribe(SubscriptionSubject subject) {
      liveServerClient.subscribeOnItem(subject);
    }

    /**
     * Tries to compact chunks - i.e, fit all subscribed subjects in lowest amount of chunks
     * possible
     */
    @Override
    public void compact() {
      if (delegate != null) {
        delegate.compact();
      }
      if (delegate != null && canBeCompacted()) {
        Collection<SubscriptionSubject> subscriptions =
            delegate.getSubscribedSubjectsMap().values();
        log.info(
            "Compacting: current chunk size: {}, delegate size: {}. Moving {} to liveserverclient {}",
            this.getChunkSize(),
            delegate.getChunkSize(),
            subscriptions,
            this.liveServerClient.getId());
        subscriptions.forEach(this::doSubscribe);

        delegate.clear();
        delegate = delegate.getDelegate();
      }
    }

    private boolean canBeCompacted() {
      int currentChunkSize = getChunkSize();
      int chunkSizeOfDelegate = delegate.getChunkSize();

      return currentChunkSize + chunkSizeOfDelegate <= maxSizeOfChunkAfterCompaction;
    }

    LiveServerClient getLiveServerClient() {
      return liveServerClient;
    }

    @Override
    public void clear() {
      log.info("Disconnecting liveserveclient {} (compacted)", liveServerClient.getId());
      liveServerClient.disconnect();
    }

    @Override
    public ChunkedNode getDelegate() {
      return delegate;
    }

    /**
     * Checks recursively if any of chunks is already subscribed to {@code subject}
     *
     * @param subject Subscription subject
     */
    @Override
    public boolean isSubscribedAlready(SubscriptionSubject subject) {
      return liveServerClient.getPayloadItems().containsKey(subject.messageHashKey())
          || (delegate != null && delegate.isSubscribedAlready(subject));
    }

    @Override
    public Map<String, SubscriptionSubject> getSubscribedSubjectsMap() {
      return liveServerClient.getPayloadItems();
    }
  }
}
