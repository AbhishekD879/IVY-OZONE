package com.ladbrokescoral.oxygen.cms.api.service.cache;

import com.ladbrokescoral.oxygen.cms.api.entity.UploadItem;
import java.util.Map;
import java.util.concurrent.ArrayBlockingQueue;
import java.util.concurrent.BlockingQueue;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.stream.IntStream;
import javax.annotation.PostConstruct;
import javax.annotation.PreDestroy;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.scheduling.concurrent.CustomizableThreadFactory;
import org.springframework.stereotype.Component;

@Slf4j
@Component
public class DeliveryNetworkExecutor {
  private static final double TEN_PERCENT = 0.1;

  private final DeliveryNetworkWorker deliveryNetworkWorker;

  private final ExecutorService executor;
  private final BlockingQueue<String> uploadPendingQueue;
  private final Map<String, UploadItem> uploadPendingItems;
  private final Integer workersCount;
  private final Integer queueCapacity;

  @Autowired
  public DeliveryNetworkExecutor(
      DeliveryNetworkWorker deliveryNetworkWorker,
      @Value("${akamai.workers.count:1}") Integer workersCount,
      @Value("${akamai.queue.size:100}") Integer queueCapacity) {
    this.deliveryNetworkWorker = deliveryNetworkWorker;
    this.workersCount = workersCount;

    uploadPendingQueue = new ArrayBlockingQueue<>(queueCapacity);
    uploadPendingItems = new ConcurrentHashMap<>(queueCapacity);
    executor =
        Executors.newFixedThreadPool(
            workersCount, new CustomizableThreadFactory("deliveryNetwork-"));
    this.queueCapacity = queueCapacity;
  }

  @PostConstruct
  public void runUploadWorkers() {
    IntStream.range(0, workersCount).forEach(w -> executor.execute(this::deliverIndefinitely));
  }

  @PreDestroy
  public void shutdown() {
    executor.shutdownNow();
  }

  private void deliverIndefinitely() {
    while (!Thread.currentThread().isInterrupted()) {
      try {
        UploadItem item = uploadPendingItems.remove(uploadPendingQueue.take());
        deliveryNetworkWorker.deliverItem(item);
        monitorQueueCapacityEnding();
      } catch (Exception e) {
        log.error("Error during uploading content", e);
      }
    }
  }

  private void monitorQueueCapacityEnding() {
    if (uploadPendingQueue.remainingCapacity() < TEN_PERCENT * queueCapacity) {
      log.warn(
          "Pending queue is almost full, remaining capacity; {}",
          uploadPendingQueue.remainingCapacity());
    }
  }

  public void addItem(UploadItem item) throws InterruptedException {
    String itemKey = item.getKeyName();
    uploadPendingItems.put(itemKey, item);
    uploadPendingQueue.put(itemKey);
  }
}
