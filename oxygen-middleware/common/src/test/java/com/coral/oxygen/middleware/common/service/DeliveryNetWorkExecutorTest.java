package com.coral.oxygen.middleware.common.service;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.*;

import com.coral.oxygen.middleware.common.configuration.cfcache.DeliveryNetworkExecutor;
import com.coral.oxygen.middleware.common.configuration.cfcache.DeliveryNetworkWorker;
import com.coral.oxygen.middleware.pojos.model.cache.UploadItem;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.ThreadPoolExecutor;
import java.util.concurrent.TimeUnit;
import java.util.stream.IntStream;
import org.junit.After;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.springframework.test.context.junit4.SpringRunner;
import org.springframework.test.util.ReflectionTestUtils;

@RunWith(SpringRunner.class)
public class DeliveryNetWorkExecutorTest {
  DeliveryNetworkExecutor deliveryNetworkExecutor;
  @Mock private DeliveryNetworkWorker deliveryNetworkWorker;

  @Before
  public void init() throws Exception {
    deliveryNetworkExecutor = new DeliveryNetworkExecutor(deliveryNetworkWorker, 1, 1, 2);
    deliveryNetworkExecutor.runUploadWorkers();
  }

  @Test
  public void addItem() throws InterruptedException {
    CountDownLatch latch = new CountDownLatch(1);
    IntStream.range(0, 5)
        .forEach(
            x -> {
              try {
                deliveryNetworkExecutor.addItem(
                    UploadItem.builder()
                        .brand("bma")
                        .action(UploadItem.Action.UPLOAD)
                        .path("/home/" + x)
                        .json("")
                        .fileName("test.json")
                        .build());
              } catch (InterruptedException e) {
                throw new RuntimeException(e);
              }
            });
    latch.await(5, TimeUnit.SECONDS);
    verify(deliveryNetworkWorker, Mockito.times(5)).deliverItem(any());
  }

  @Test
  public void addItemWithInterreputException() throws InterruptedException {
    deliveryNetworkExecutor.runUploadWorkers();
    CountDownLatch latch = new CountDownLatch(1);
    IntStream.range(0, 5)
        .forEach(
            x -> {
              try {
                deliveryNetworkExecutor.addItem(
                    UploadItem.builder()
                        .brand("bma")
                        .action(UploadItem.Action.UPLOAD)
                        .path("/home/" + x)
                        .json("")
                        .fileName("test.json")
                        .build());
              } catch (InterruptedException e) {
                throw new RuntimeException(e);
              }
            });
    deliveryNetworkExecutor.shutdown();
    latch.await(2, TimeUnit.SECONDS);
    verify(deliveryNetworkWorker, atLeastOnce()).deliverItem(any());
  }

  @Test
  public void addItemWithException() throws InterruptedException {
    ThreadPoolExecutor uploadExecutor = mock(ThreadPoolExecutor.class);
    ReflectionTestUtils.setField(deliveryNetworkExecutor, "uploadExecutor", uploadExecutor);
    Mockito.doThrow(NullPointerException.class).when(uploadExecutor).execute(any());
    CountDownLatch latch = new CountDownLatch(1);

    IntStream.range(0, 5)
        .forEach(
            x -> {
              try {
                deliveryNetworkExecutor.addItem(
                    UploadItem.builder()
                        .brand("bma")
                        .action(UploadItem.Action.UPLOAD)
                        .path("/home/" + x)
                        .json("")
                        .fileName("test.json")
                        .build());
              } catch (InterruptedException e) {
                throw new RuntimeException(e);
              }
            });
    latch.await(5, TimeUnit.SECONDS);
    verify(deliveryNetworkWorker, never()).deliverItem(any());
  }

  @After
  public void shutdown() {
    deliveryNetworkExecutor.shutdown();
  }
}
