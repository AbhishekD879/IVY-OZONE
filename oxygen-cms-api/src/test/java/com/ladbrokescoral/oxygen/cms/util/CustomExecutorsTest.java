package com.ladbrokescoral.oxygen.cms.util;

import java.util.concurrent.ExecutorService;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.atomic.AtomicInteger;
import org.junit.Assert;
import org.junit.Test;

public class CustomExecutorsTest {

  private CustomExecutors customExecutors = new CustomExecutors();

  @Test
  public void newSingleThreadLastTaskExecutorCase1() throws InterruptedException {
    ExecutorService service = customExecutors.newSingleThreadLastTaskExecutor();
    AtomicInteger counter = new AtomicInteger();
    StringBuilder builder = new StringBuilder();
    service.execute(new MyRunnable("A", counter, builder));
    service.execute(new MyRunnable("B", counter, builder));
    service.execute(new MyRunnable("C", counter, builder));
    service.execute(new MyRunnable("D", counter, builder));
    service.execute(new MyRunnable("F", counter, builder));
    sleep(150);
    service.awaitTermination(150, TimeUnit.MILLISECONDS);
    Assert.assertEquals(2, counter.get());
    Assert.assertEquals("AF", builder.toString());
  }

  @Test
  public void newSingleThreadLastTaskExecutorCase2() throws InterruptedException {
    ExecutorService service = customExecutors.getSingleThreadLastTaskExecutor("test");
    AtomicInteger counter = new AtomicInteger();
    StringBuilder builder = new StringBuilder();
    service.execute(new MyRunnable("A", counter, builder));
    sleep(10);
    service.execute(new MyRunnable("B", counter, builder));
    sleep(10);
    service.execute(new MyRunnable("C", counter, builder));
    sleep(10);
    service.execute(new MyRunnable("D", counter, builder));
    sleep(10);
    service.execute(new MyRunnable("E", counter, builder));
    service.awaitTermination(250, TimeUnit.MILLISECONDS);
    Assert.assertEquals(2, counter.get());
    Assert.assertEquals("AE", builder.toString());
  }

  private class MyRunnable implements Runnable {

    private String name;
    private AtomicInteger counter;
    private StringBuilder builder;

    public MyRunnable(String name, AtomicInteger counter, StringBuilder builder) {
      this.name = name;
      this.counter = counter;
      this.builder = builder;
    }

    @Override
    public void run() {
      sleep(100);
      counter.incrementAndGet();
      builder.append(name);
    }
  }

  private void sleep(int l) {
    try {
      Thread.sleep(l);
    } catch (InterruptedException e) {
      e.printStackTrace();
    }
  }
}
