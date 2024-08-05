package com.coral.oxygen.middleware.common.service;

import static org.mockito.ArgumentMatchers.any;

import com.coral.oxygen.middleware.common.configuration.cfcache.DeliveryNetworkExecutor;
import com.coral.oxygen.middleware.common.configuration.cfcache.DeliveryNetworkService;
import com.coral.oxygen.middleware.common.configuration.cfcache.DeliveryNetworkServiceImpl;
import com.coral.oxygen.middleware.common.configuration.cfcache.DeliveryNetworkWorker;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.ObjectWriter;
import org.junit.After;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.springframework.test.context.junit4.SpringRunner;

@RunWith(SpringRunner.class)
public class DeliveryNetworkServiceTest {

  @Mock DeliveryNetworkExecutor deliveryNetworkExecutor;
  DeliveryNetworkService deliveryNetworkService;
  ObjectMapper mapper = new ObjectMapper();
  ObjectWriter writer = mapper.writer();
  @Mock private DeliveryNetworkWorker deliveryNetworkWorker;

  @Before
  public void init() throws Exception {
    deliveryNetworkService = new DeliveryNetworkServiceImpl(deliveryNetworkExecutor, writer);
    deliveryNetworkExecutor.runUploadWorkers();
  }

  @Test
  public void uploadItem() throws InterruptedException {
    deliveryNetworkService.upload("bma", "/home/", "test.json", "");
    Mockito.verify(deliveryNetworkExecutor, Mockito.times(1)).addItem(any());
  }

  @Test
  public void addItemWithException() throws InterruptedException {
    Mockito.doThrow(NullPointerException.class).when(deliveryNetworkExecutor).addItem(any());
    deliveryNetworkService.upload("bma", "//home/", "test.json", "");
    Mockito.verify(deliveryNetworkExecutor, Mockito.times(1)).addItem(any());
  }

  @Test
  public void addItemWithInterreputException() throws InterruptedException {
    Mockito.doThrow(InterruptedException.class).when(deliveryNetworkExecutor).addItem(any());
    deliveryNetworkService.upload("bma", "/home/", "test.json", "");
    Mockito.verify(deliveryNetworkExecutor, Mockito.times(1)).addItem(any());
  }

  @After
  public void shutdown() {
    deliveryNetworkExecutor.shutdown();
  }
}
