package com.ladbrokescoral.oxygen.cms.api.service.cache;

import static org.mockito.Mockito.*;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectWriter;
import com.ladbrokescoral.oxygen.cms.api.entity.UploadItem;
import com.ladbrokescoral.oxygen.cms.configuration.CFCacheTagProperties;
import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;
import org.slf4j.Logger;

@RunWith(MockitoJUnitRunner.Silent.class)
public class DeliveryNetworkServiceImplTest {
  DeliveryNetworkExecutor deliveryNetworkExecutor = mock(DeliveryNetworkExecutor.class);
  ObjectWriter objectWriter = mock(ObjectWriter.class);
  CFCacheTagProperties cfCacheTagProperties = mock(CFCacheTagProperties.class);

  @Mock Logger logger;

  @InjectMocks
  DeliveryNetworkServiceImpl deliveryNetworkService =
      new DeliveryNetworkServiceImpl(deliveryNetworkExecutor, objectWriter, cfCacheTagProperties);

  @Before
  public void setUp() {}

  @Test
  public void testUpload() throws JsonProcessingException, InterruptedException {
    when(objectWriter.writeValueAsString(any())).thenReturn("string");
    doNothing().when(deliveryNetworkExecutor).addItem(any());
    Assert.assertNotNull(deliveryNetworkService);
    deliveryNetworkService.upload("bma", "/", "", "");
  }

  @Test
  public void testUploadWithException() throws JsonProcessingException, InterruptedException {
    when(objectWriter.writeValueAsString(any())).thenReturn("string");
    doThrow(NullPointerException.class).when(deliveryNetworkExecutor).addItem(any());
    Assert.assertNotNull(deliveryNetworkService);
    deliveryNetworkService.upload("bma", "/", "", "");
  }

  @Test
  public void testUploadWithInterruptedException()
      throws JsonProcessingException, InterruptedException {
    when(objectWriter.writeValueAsString(any())).thenReturn("string");
    doThrow(InterruptedException.class)
        .when(deliveryNetworkExecutor)
        .addItem(any(UploadItem.class));
    Assert.assertNotNull(deliveryNetworkService);
    deliveryNetworkService.upload("bma", "/", "", "");
  }

  @Test
  public void testDelete() throws JsonProcessingException, InterruptedException {
    when(objectWriter.writeValueAsString(any())).thenReturn("string");
    doNothing().when(deliveryNetworkExecutor).addItem(any());
    Assert.assertNotNull(deliveryNetworkService);
    deliveryNetworkService.delete("bma", "/", "");
  }

  @Test
  public void testDeleteWithException() throws JsonProcessingException, InterruptedException {
    when(objectWriter.writeValueAsString(any())).thenReturn("string");
    doThrow(NullPointerException.class).when(deliveryNetworkExecutor).addItem(any());
    Assert.assertNotNull(deliveryNetworkService);
    deliveryNetworkService.delete("bma", "/", "");
  }

  @Test
  public void testDeleteWithInterruptedException()
      throws JsonProcessingException, InterruptedException {
    when(objectWriter.writeValueAsString(any())).thenReturn("string");
    doThrow(InterruptedException.class)
        .when(deliveryNetworkExecutor)
        .addItem(any(UploadItem.class));
    Assert.assertNotNull(deliveryNetworkService);
    deliveryNetworkService.delete("bma", "/", "");
  }

  @Test
  public void testUploadCFContent() throws JsonProcessingException, InterruptedException {
    when(objectWriter.writeValueAsString(any())).thenReturn("string");
    doNothing().when(deliveryNetworkExecutor).addItem(any());
    Assert.assertNotNull(deliveryNetworkService);
    deliveryNetworkService.uploadCFContent("bma", "/", "", "");
  }

  @Test
  public void testUploadCFContentWithInterruptedException()
      throws JsonProcessingException, InterruptedException {
    when(objectWriter.writeValueAsString(any())).thenReturn("string");
    doThrow(InterruptedException.class)
        .when(deliveryNetworkExecutor)
        .addItem(any(UploadItem.class));
    Assert.assertNotNull(deliveryNetworkService);
    deliveryNetworkService.uploadCFContent("bma", "/", "", "");
  }

  @Test
  public void testUploadCFContentWithException()
      throws JsonProcessingException, InterruptedException {
    when(objectWriter.writeValueAsString(any())).thenReturn("string");
    doThrow(NullPointerException.class)
        .when(deliveryNetworkExecutor)
        .addItem(any(UploadItem.class));
    Assert.assertNotNull(deliveryNetworkService);
    deliveryNetworkService.uploadCFContent("bma", "/", "", "");
  }
}
