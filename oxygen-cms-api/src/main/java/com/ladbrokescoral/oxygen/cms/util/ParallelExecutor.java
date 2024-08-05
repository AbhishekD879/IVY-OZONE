package com.ladbrokescoral.oxygen.cms.util;

import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.stream.Stream;

public class ParallelExecutor {

  private ExecutorService executorService = Executors.newCachedThreadPool();

  private void add(List<CompletableFuture<?>> completableFutures, Runnable runnable) {
    CompletableFuture<?> completableFuture =
        CompletableFuture.supplyAsync(
            () -> {
              runnable.run();
              return null;
            },
            executorService);
    completableFutures.add(completableFuture);
  }

  private void add(List<CompletableFuture<?>> completableFutures, Runnable... runnable) {
    Stream.of(runnable).forEach(action -> add(completableFutures, action));
  }

  public void execute(Runnable... runnables) throws InterruptedException, ExecutionException {
    List<CompletableFuture<?>> completableFutures = new ArrayList<>();
    add(completableFutures, runnables);
    CompletableFuture<?>[] futures = completableFutures.stream().toArray(CompletableFuture[]::new);
    CompletableFuture.allOf(futures).get();
  }
}
