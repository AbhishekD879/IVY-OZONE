package com.coral.oxygen.edp.tracking;

import java.util.HashSet;
import java.util.Map;
import java.util.Set;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.atomic.AtomicInteger;
import lombok.extern.slf4j.Slf4j;
import org.eclipse.jetty.util.BlockingArrayQueue;

@Slf4j
public abstract class QueuedMultiThreadDataConsumer<T, D> implements DataConsumer<T, D> {

  private final BlockingArrayQueue<Set<T>> tasksQueue;

  private final Object queueReadingLock = new Object();

  private final ExecutorService executor;

  private final Set<T> ticketsUnderConsuming;

  private final Object underConsumingLock = new Object();

  private ConsumingListener<T, D> listener;

  public QueuedMultiThreadDataConsumer(int maxQueueSize, int threadsCount) {
    this.tasksQueue = new BlockingArrayQueue<>(maxQueueSize);
    this.ticketsUnderConsuming = new HashSet<>();
    AtomicInteger atomicInteger = new AtomicInteger(0);
    this.executor =
        Executors.newFixedThreadPool(
            threadsCount,
            r -> {
              Thread t = new Thread(r);
              t.setDaemon(true);
              t.setName("QueuedMultiThreadDataConsumer executor " + atomicInteger.addAndGet(1));
              return t;
            });
    for (int i = 0; i < threadsCount; i++) {
      executor.submit(
          () -> {
            log.info("Starting consumer thread");
            try {
              while (!Thread.currentThread().isInterrupted()) {
                processQueue();
              }
            } catch (InterruptedException e) {
              log.info("Consuming thread is interrupted", e);
              Thread.currentThread().interrupt();
            }
          });
    }
  }

  @Override
  public void consume(Set<T> consumingTask) {
    Set<T> filteredTasks = excludeUnderConsuming(consumingTask);
    if (filteredTasks.isEmpty()) {
      // all new tasks are under consuming right now. Nothing new to consume
      return;
    }
    if (!tasksQueue.offer(consumingTask)) {
      String message = "Consuming queue is full. Max size: " + tasksQueue.getMaxCapacity();
      sendError(message, new IllegalStateException(message));
    }
  }

  @Override
  public void setListener(ConsumingListener<T, D> listener) {
    this.listener = listener;
  }

  protected void processQueue() throws InterruptedException {
    Set<T> tasks = getTicketsFromQueue();
    safeConsuming(tasks);
  }

  private void safeConsuming(Set<T> tickets) {
    try {
      Map<T, D> consumedData;
      try {
        consumedData = doConsume(tickets);
        listener.onResponse(consumedData);
      } finally {
        removeFromUnderConsuming(tickets);
      }
    } catch (Exception e) {
      log.error("Consuming error", e);
      sendError("Consuming error", e);
    }
  }

  private Set<T> getTicketsFromQueue() throws InterruptedException {
    synchronized (queueReadingLock) {
      log.info("Waiting for tasks");
      Set<T> tasks = new HashSet<>(tasksQueue.take());
      log.info("New tasks {}", tasks);
      while (!tasksQueue.isEmpty()) {
        Set<T> poll = tasksQueue.poll();
        log.info("Merging tasks {}", poll);
        tasks.addAll(poll);
      }
      addToUnderConsuming(tasks);
      return tasks;
    }
  }

  protected void sendError(String message, Throwable t) {
    if (listener != null) {
      listener.onError(message, t);
    }
  }

  private void addToUnderConsuming(Set<T> tickets) {
    synchronized (underConsumingLock) {
      ticketsUnderConsuming.addAll(tickets);
    }
  }

  private void removeFromUnderConsuming(Set<T> tickets) {
    synchronized (underConsumingLock) {
      ticketsUnderConsuming.removeAll(tickets);
    }
  }

  private Set<T> excludeUnderConsuming(Set<T> tickets) {
    synchronized (underConsumingLock) {
      Set<T> result = new HashSet<>(tickets);
      result.removeAll(ticketsUnderConsuming);
      return result;
    }
  }

  protected abstract Map<T, D> doConsume(Set<T> tickets);
}
