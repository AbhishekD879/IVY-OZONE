package com.ladbrokescoral.oxygen.cms.util;

import java.util.concurrent.ExecutionException;
import java.util.concurrent.atomic.AtomicInteger;
import org.junit.Assert;
import org.junit.Test;

public class ParallelExecutorTest {

  @Test
  public void testExecute() throws InterruptedException, ExecutionException {
    AtomicInteger integer1 = new AtomicInteger();
    AtomicInteger integer2 = new AtomicInteger();
    ParallelExecutor executor = new ParallelExecutor();
    Runnable runnable1 =
        () -> {
          integer1.set(20);
        };
    Runnable runnable2 =
        () -> {
          integer2.set(200);
        };
    executor.execute(runnable1, runnable2);
    Assert.assertEquals(200, integer2.get());
    Assert.assertEquals(20, integer1.get());
  }

  @Test
  public void testExecuteList() throws InterruptedException, ExecutionException {
    AtomicInteger integer1 = new AtomicInteger();
    AtomicInteger integer2 = new AtomicInteger();
    ParallelExecutor executor = new ParallelExecutor();
    executor.execute(
        () -> {
          integer1.set(20);
        },
        () -> {
          integer2.set(200);
        });
    Assert.assertEquals(200, integer2.get());
    Assert.assertEquals(20, integer1.get());
  }
}
