package com.egalacoral.spark.timeform.api.connectivity;

import java.util.*;
import java.util.concurrent.*;
import java.util.stream.Collectors;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.egalacoral.spark.timeform.api.DataCallback;
import com.egalacoral.spark.timeform.api.TimeFormException;

import retrofit2.Call;

public class TimeLimitRequestPerformer implements RequestPerformer {

  private static final transient Logger LOGGER = LoggerFactory.getLogger(TimeLimitRequestPerformer.class);

  private final RequestPerformer delegate;

  private final TimeProvider timeProvider;

  private final ExecutorService executor;

  private final List<TimeTracker> timeTrackers;

  public TimeLimitRequestPerformer(RequestPerformer delegate, TimeProvider timeProvider,
      Map<Long, Integer> limitations) {
    this.delegate = delegate;
    this.timeProvider = timeProvider;
    this.timeTrackers = limitations.entrySet().stream()
        .map(e -> new TimeTracker(e.getValue(), e.getKey(), timeProvider)).collect(Collectors.toList());
    executor = Executors.newSingleThreadExecutor(new ThreadFactory() {
      @Override
      public Thread newThread(Runnable r) {
        Thread thread = new Thread(r, "TimeLimitRequestPerformer-Thread");
        thread.setDaemon(true);
        return thread;
      }
    });
  }

  @Override
  public <T> T invokeSync(Call<T> call) {
    try {
      return executor.submit(new CallableWrapper<T>(() -> {
        return delegate.invokeSync(call);
      })).get();
    } catch (Exception e) {
      throw prepareException(e);
    }
  }

  @Override
  public <T> void invokeAsync(Call<T> call, DataCallback<T> dataCallback) {
    try {
      executor.submit(new CallableWrapper<Void>(() -> {
        try {
          delegate.invokeAsync(call, dataCallback);
        } catch (Exception e) {
          dataCallback.onError(prepareException(e));
        }
        return null;
      }));
    } catch (Exception e) {
      dataCallback.onError(prepareException(e));
    }
  }

  private TimeFormException prepareException(Throwable t) {
    Set<Throwable> visited = new HashSet<>();
    Throwable checked = t;
    while (checked != null && !visited.contains(checked)) {
      visited.add(checked);
      if (checked instanceof TimeFormException) {
        return (TimeFormException) checked;
      }
      checked = checked.getCause();
    }
    return new TimeFormException(t);
  }

  private class CallableWrapper<T> implements Callable<T> {

    private final Callable<T> delegate;

    public CallableWrapper(Callable<T> delegate) {
      this.delegate = delegate;
    }

    @Override
    public T call() throws Exception {
      long waitTime = timeTrackers.stream() //
          .map(tt -> tt.calculateWaitTime()) //
          .mapToLong(Long::longValue) //
          .max().getAsLong();
      if (waitTime > 0) {
        LOGGER.debug("Waiting {} ms", waitTime);
        Thread.sleep(waitTime);
      }
      timeTrackers.stream().forEach(tt -> tt.addRequestTime());
      return delegate.call();
    }
  }

  public static class TimeTracker {
    private final int countLimit;
    private final long timeLimit;
    private final TimeProvider timeProvider;
    private final Queue<Long> queue;

    public TimeTracker(int countLimit, long timeLimit, TimeProvider timeProvider) {
      this.countLimit = countLimit;
      this.timeLimit = timeLimit;
      this.timeProvider = timeProvider;
      this.queue = new LinkedList<>();
    }

    public synchronized long calculateWaitTime() {
      if (queue.size() < countLimit) {
        return 0;
      }
      long spentFromLimitedRequest = (timeProvider.currentTime() - queue.peek());
      return Math.max(0, timeLimit - spentFromLimitedRequest);
    }

    public synchronized void addRequestTime() {
      queue.offer(timeProvider.currentTime());
      while (queue.size() > countLimit) {
        queue.poll();
      }
    }
  }

}
