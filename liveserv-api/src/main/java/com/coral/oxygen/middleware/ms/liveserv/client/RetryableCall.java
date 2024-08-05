package com.coral.oxygen.middleware.ms.liveserv.client;

import com.coral.oxygen.middleware.ms.liveserv.exceptions.RequestFailedException;
import com.coral.oxygen.middleware.ms.liveserv.exceptions.ServiceException;
import java.io.IOException;
import java.io.InterruptedIOException;
import lombok.extern.slf4j.Slf4j;

/** Created by azayats on 18.05.17. */
@Slf4j
public class RetryableCall implements Call {

  private static final int DEFAULT_RETRIES_COUNT = 10;
  private static final int DEFAULT_RETRIES_DELAY = 1000;

  private final Call delegate;

  private int retriesCount = DEFAULT_RETRIES_COUNT;

  // TODO: can we use circuit breaker
  private long retriesDelay = DEFAULT_RETRIES_DELAY;

  public RetryableCall(Call delegate) {
    this.delegate = delegate;
  }

  @Override
  public String execute(String request) throws IOException, InterruptedException, ServiceException {
    Exception lastException = null;
    for (int i = 0; i <= retriesCount; i++) {
      try {
        return delegate.execute(request);
      } catch (InterruptedIOException e) {
        throw e;
      } catch (IOException e) {
        InterruptedException interruptedCause = findInterruptedException(e);
        if (interruptedCause != null) {
          throw new InterruptedException("Interrupted Inside delegate.");
        }
        lastException = e;
        log.error("Request failed. Retry index:{}, {}", i, e);
        if (i < retriesCount) {
          int sleepIndex = i + 1;
          log.warn("Sleeping before retry {} ms", retriesDelay * sleepIndex);
          try {
            Thread.sleep(retriesDelay * sleepIndex);
          } catch (InterruptedException interruptedException) {
            log.error("Interrupted.", interruptedException);
            Thread.currentThread().interrupt();
            throw new InterruptedException("Interrupted on sleepp after IO error.");
          }
        }
      }
    }
    throw new RequestFailedException(
        "Request failed after " + retriesCount + " retries.", lastException);
  }

  public void setRetriesCount(int retriesCount) {
    this.retriesCount = retriesCount;
  }

  public void setRetriesDelay(long retriesDelay) {
    this.retriesDelay = retriesDelay;
  }

  private InterruptedException findInterruptedException(Throwable t) {
    Throwable candidate = t;
    do {
      if (t instanceof InterruptedException) {
        return (InterruptedException) t;
      } else {
        t = t.getCause();
      }
    } while (t != null);
    return null;
  }
}
