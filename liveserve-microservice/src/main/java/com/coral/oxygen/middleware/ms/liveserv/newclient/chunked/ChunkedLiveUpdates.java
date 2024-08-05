package com.coral.oxygen.middleware.ms.liveserv.newclient.chunked;

import com.coral.oxygen.middleware.ms.liveserv.newclient.LiveUpdatesChannel;
import com.coral.oxygen.middleware.ms.liveserv.newclient.liveserve.LiveServerClient;
import com.coral.oxygen.middleware.ms.liveserv.newclient.liveserve.LiveServerClientBuilder;
import com.newrelic.api.agent.NewRelic;
import java.util.*;
import java.util.function.Supplier;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

/**
 * Subscribes on liveserve channels with breaking them in chunks of predefined size if needed;
 *
 * <p>If chunk's size has been reached, new chunk will be created dynamically. Vice versa, subjects
 * will be moved to one chunk if they fit it
 *
 * @author volodymyr.masliy
 */
@Component
@Slf4j
public class ChunkedLiveUpdates {
  /**
   * Given two chunks, if sum of their subjects is less then FILL_FACTOR *
   * numOfSubjectsInOneMessage, then these chunks can be compacted. See #{@link
   * ChunkedLiveServerNode#compact()}
   */
  private static final double FILL_FACTOR = 0.75;

  private final int numOfSubjectsInOneMessage;
  private final int maxSizeOfChunkAfterCompaction;
  private ChunkedNode rootNode;
  private Supplier<LiveServerClient> liveServerClientSupplier;

  @Autowired
  public ChunkedLiveUpdates(
      @Value("${liveServer.subscription.limitPerClient:200}") int numOfSubjectsInOneMessage,
      LiveServerClientBuilder liveServerClientBuilder) {
    this.numOfSubjectsInOneMessage = numOfSubjectsInOneMessage;
    this.maxSizeOfChunkAfterCompaction = (int) (FILL_FACTOR * numOfSubjectsInOneMessage);
    this.liveServerClientSupplier = liveServerClientBuilder::build;
    this.rootNode = new ChunkedLiveServerNode(liveServerClientSupplier.get());
  }

  public void subscribeOnItem(LiveUpdatesChannel subject) {
    rootNode.subscribe(subject);
  }

  public void unsubscribe(LiveUpdatesChannel channel) {
    rootNode.unsubscribe(channel);
  }

  public Map<String, Object> getChunksStats() {
    Map<String, Object> stats = new HashMap<>();
    List<Integer> channelsPerChunk = new ArrayList<>();
    ChunkedNode node = rootNode;
    int numOfChunks = 0;
    while (node != null) {
      channelsPerChunk.add(node.getChunkSize());
      node = node.getDelegate();
      numOfChunks++;
    }
    stats.put("channelsPerChunk", channelsPerChunk);
    stats.put("numOfChunks", numOfChunks);
    return stats;
  }

  //  @Override
  public Map<String, LiveUpdatesChannel> getPayloadItems() {
    Map<String, LiveUpdatesChannel> subs = new HashMap<>();
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
    public void subscribe(LiveUpdatesChannel subject) {
      if (isSubscribedAlready(subject)) {
        return;
      }

      if (!isMaxChunkSizeReached()) {
        doSubscribe(subject);
        compact();
      } else {
        if (delegate == null) {
          LiveServerClient newLiveServerClient = liveServerClientSupplier.get();
          log.info(
              "Max chunk size has been reached for LiveServerClient <{}>. Creating LiveServerClient <{}>. Was adding {}",
              liveServerClient.getId(),
              newLiveServerClient.getId(),
              subject);
          NewRelic.recordMetric("Creating LiveServerClient chunk", 1);
          delegate = new ChunkedLiveServerNode(newLiveServerClient);
        }
        delegate.subscribe(subject);
      }

      if (!liveServerClient.isRunning()) {
        liveServerClient.connect();
      }
    }

    @Override
    public void unsubscribe(LiveUpdatesChannel subject) {
      if (isChannelExistsInThisChunk(subject)) {
        liveServerClient.unsubscribe(subject);
      } else if (delegate != null) {
        delegate.unsubscribe(subject);
      }
    }

    private void doSubscribe(LiveUpdatesChannel subject) {
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
        Collection<LiveUpdatesChannel> subscriptions = delegate.getSubscribedSubjectsMap().values();
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
    public boolean isSubscribedAlready(LiveUpdatesChannel subject) {
      return isChannelExistsInThisChunk(subject)
          || (delegate != null && delegate.isSubscribedAlready(subject));
    }

    private boolean isChannelExistsInThisChunk(LiveUpdatesChannel subject) {
      return liveServerClient.getPayloadItems().containsKey(subject.messageHashKey());
    }

    @Override
    public Map<String, LiveUpdatesChannel> getSubscribedSubjectsMap() {
      return liveServerClient.getPayloadItems();
    }
  }
}
