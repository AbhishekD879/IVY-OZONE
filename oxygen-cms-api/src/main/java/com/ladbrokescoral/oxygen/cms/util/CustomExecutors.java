package com.ladbrokescoral.oxygen.cms.util;

import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.ConcurrentMap;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.LinkedBlockingQueue;
import java.util.concurrent.RejectedExecutionHandler;
import java.util.concurrent.ThreadPoolExecutor;
import java.util.concurrent.TimeUnit;
import org.springframework.util.ObjectUtils;

public class CustomExecutors {

  private ConcurrentMap<String, ExecutorService> keyedExecutors = new ConcurrentHashMap<>();

  /**
   * This executor ignores all similar tasks but last one to avoid flooding.
   *
   * @return instance of the ExecutorService
   */
  public ExecutorService newSingleThreadLastTaskExecutor() {
    RejectedExecutionHandler handler = new ThreadPoolExecutor.DiscardOldestPolicy();
    LinkedBlockingQueue workQueue = new LastTaskLinkedBlockingQueue();
    return new ThreadPoolExecutor(1, 1, 0L, TimeUnit.MILLISECONDS, workQueue, handler);
  }

  public ExecutorService getSingleThreadLastTaskExecutor(String key) {
    ExecutorService executorService = keyedExecutors.get(key);

    if (ObjectUtils.isEmpty(executorService)) {
      executorService = newSingleThreadLastTaskExecutor();
      keyedExecutors.put(key, executorService);
    }

    return executorService;
  }

  private class LastTaskLinkedBlockingQueue extends LinkedBlockingQueue {
    public LastTaskLinkedBlockingQueue() {
      super(1);
    }

    @Override
    public void put(Object o) throws InterruptedException {
      clear();
      super.put(o);
    }
  }
}
