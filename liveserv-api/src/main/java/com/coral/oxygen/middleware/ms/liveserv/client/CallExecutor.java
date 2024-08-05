package com.coral.oxygen.middleware.ms.liveserv.client;

import com.coral.oxygen.middleware.ms.liveserv.client.model.Message;
import com.coral.oxygen.middleware.ms.liveserv.model.SubscriptionStats;
import java.io.InterruptedIOException;
import java.util.Collection;
import java.util.Collections;
import java.util.List;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;
import java.util.function.Supplier;
import lombok.extern.slf4j.Slf4j;

/**
 * This class executes calls to Live Server L
 *
 * @author Vitalij Havryk
 */
@Slf4j
public class CallExecutor {

  private static final int WAIT_TIME_MILLIS = 5000;
  public static final int MAX_ERRORS_COUNT = 10;
  public static final int AWAIT_TERMINATION_SECONDS = 2;
  private final Call call;
  private final Supplier<Collection<SubscriptionStats>> subscriptionsSupplier;
  private final LiveServerListener listener;
  private final ExecutorService executorService;
  private volatile boolean stopped;
  private long waitSubscriptionInterval = WAIT_TIME_MILLIS;
  private long sleepAfterErrorTime = WAIT_TIME_MILLIS;
  private long errorCount = 0;

  private final Object waitSubscriptionsLock = new Object();

  public CallExecutor(
      Call call,
      Supplier<Collection<SubscriptionStats>> subscriptionsSupplier,
      LiveServerListener listeners) {
    this.call = call;
    this.listener = listeners;
    this.subscriptionsSupplier = subscriptionsSupplier;
    executorService =
        Executors.newSingleThreadExecutor(
            (Runnable r) -> {
              Thread thread = new Thread(r);
              thread.setName("LiveServ CallExecutor thread");
              thread.setDaemon(true);
              return thread;
            });
  }

  public void execute() {
    executorService.execute(this::infinityExecute);
  }

  private void infinityExecute() {
    do {
      try {
        doExecute();
      } catch (InterruptedIOException e) {
        log.error("Interrupted IO to LiveServ", e);
      } catch (InterruptedException e) {
        // TODO:need to clarify this behaviour
        log.error("Interrupted call to LiveServ ", e);
        stopped = true;
        Thread.currentThread().interrupt();
      }
    } while (!stopped);
  }

  private Collection<SubscriptionStats> getSubscriptionsWithWait() throws InterruptedException {
    Collection<SubscriptionStats> result;
    while ((result = subscriptionsSupplier.get()).isEmpty() && !stopped) {
      log.info("There are no items to subscribe");
      log.debug("Waiting {} miliseconds...", waitSubscriptionInterval);
      synchronized (waitSubscriptionsLock) {
        waitSubscriptionsLock.wait(waitSubscriptionInterval);
      }
    }
    if (stopped) {
      result = Collections.emptyList();
    }
    return result;
  }

  public void notifyAboutNewSubscription() {
    synchronized (waitSubscriptionsLock) {
      waitSubscriptionsLock.notifyAll();
    }
  }

  private void doExecute() throws InterruptedException, InterruptedIOException {
    Collection<SubscriptionStats> subscriptionStats = getSubscriptionsWithWait();
    if (subscriptionStats.isEmpty()) return;
    RequestBuilder builder = new RequestBuilder();
    String requestBody = builder.build(subscriptionStats);

    try {
      log.info("Getting LiveUpdates for {}", requestBody);
      String response = call.execute(requestBody);
      ResponseConverter converter = new ResponseConverter();
      List<Message> messages = converter.convert(response);
      listener.onMessages(messages);
    } catch (InterruptedIOException e) {
      log.error("InterruptedIOException during call to LiveServ", e);
      throw new InterruptedIOException("Interrupted due to IO exception");
    } catch (Exception e) {
      log.error("Error during call to to LiveServ", e);
      InterruptedException interruptedException = findInterruptedException(e);
      if (interruptedException != null) {
        throw interruptedException;
      } else {
        listener.onError(subscriptionStats, e);
        errorCount = errorCount >= MAX_ERRORS_COUNT ? 0 : errorCount;
        errorCount++;
        log.warn("Sleeping after error {} miliseconds...", sleepAfterErrorTime * errorCount);
        Thread.sleep(sleepAfterErrorTime * errorCount);
      }
    }
  }

  private InterruptedException findInterruptedException(Throwable t) {
    do {
      if (t instanceof InterruptedException) {
        return (InterruptedException) t;
      } else {
        t = t.getCause();
      }
    } while (t != null);
    return null;
  }

  public void shutdown() throws InterruptedException {
    stopped = true;
    executorService.shutdown();
    executorService.awaitTermination(AWAIT_TERMINATION_SECONDS, TimeUnit.SECONDS);
  }

  public void setWaitSubscriptionInterval(long waitSubscriptionInterval) {
    this.waitSubscriptionInterval = waitSubscriptionInterval;
  }

  public void setSleepAfterErrorTime(long sleepAfterErrorTime) {
    this.sleepAfterErrorTime = sleepAfterErrorTime;
  }
}
