package com.coral.oxygen.middleware.common.service;

import static org.mockito.Mockito.*;

import com.amazonaws.SdkClientException;
import com.amazonaws.services.s3.AmazonS3;
import com.coral.oxygen.middleware.common.configuration.cfcache.AmazonS3ServiceImpl;
import com.coral.oxygen.middleware.common.configuration.cfcache.CachePurgeService;
import java.lang.reflect.Constructor;
import java.lang.reflect.InvocationTargetException;
import java.net.InetAddress;
import java.net.UnknownHostException;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.MockedStatic;
import org.mockito.junit.MockitoJUnitRunner;

@RunWith(MockitoJUnitRunner.class)
public class AmazonS3ServiceTest {
  private final String TYPE = "s3";
  private final String BRAND = "bma";
  private final String PATH = "http://sports.coral.co.uk//";
  @Mock private CachePurgeService cachePurgeService;
  @Mock private AmazonS3 amazonS3;
  @InjectMocks private AmazonS3ServiceImpl service;
  @InjectMocks private AmazonS3ServiceImpl pathWithSlashService;

  @Before
  public void init() throws Exception {
    Constructor<AmazonS3ServiceImpl> constructor =
        AmazonS3ServiceImpl.class.getDeclaredConstructor(
            AmazonS3.class, String.class, String.class, CachePurgeService.class);
    constructor.setAccessible(true);
    service = constructor.newInstance(amazonS3, TYPE, PATH, cachePurgeService);
    pathWithSlashService = constructor.newInstance(amazonS3, TYPE, "/" + PATH, cachePurgeService);
  }

  @Test
  public void testToGetMasterDataByLineItem() {
    doNothing().when(cachePurgeService).purgeCache(BRAND, PATH, "");
    service.purgeCache(BRAND, PATH, "");
    verify(cachePurgeService, times(1)).purgeCache(BRAND, PATH, "");
  }

  @Test
  public void uploadJSONTest() {
    pathWithSlashService.uploadJSON(BRAND, PATH, "");
    verify(amazonS3, times(1)).putObject(any());
  }

  @Test
  public void uploadJSONSdkClientException() {
    doThrow(new SdkClientException("Exception")).when(amazonS3).putObject(any());
    service.uploadJSON(BRAND, PATH, "");
    verify(amazonS3, times(1)).putObject(any());
  }

  @Test
  public void uploadJSONNullPointerException() {
    service.uploadJSON(BRAND, PATH, null);
    verify(amazonS3, times(0)).putObject(any());
  }

  @Test
  public void InetAdressTest()
      throws NoSuchMethodException, InvocationTargetException, InstantiationException,
          IllegalAccessException {

    try (MockedStatic mocked = mockStatic(InetAddress.class)) {
      mocked.when(() -> InetAddress.getLocalHost()).thenThrow(UnknownHostException.class);
      Constructor<AmazonS3ServiceImpl> constructor =
          AmazonS3ServiceImpl.class.getDeclaredConstructor(
              AmazonS3.class, String.class, String.class, CachePurgeService.class);
      constructor.setAccessible(true);
      service = constructor.newInstance(amazonS3, TYPE, PATH, cachePurgeService);
      verify(amazonS3, times(0)).putObject(any());
    }
  }

  @Test
  public void shutdownTest() {
    service.shutdown();
    verify(cachePurgeService, times(1)).shutdown();
  }

  @Test
  public void purgeCacheTest() {
    service.purgeCache(BRAND, PATH, "");
    verify(cachePurgeService, times(1)).purgeCache(anyString(), anyString(), anyString());
  }

  @Test
  public void getRootUrlTest() {
    service.getRootUrl();
    verify(cachePurgeService, times(1)).getRootUrl();
  }
}
