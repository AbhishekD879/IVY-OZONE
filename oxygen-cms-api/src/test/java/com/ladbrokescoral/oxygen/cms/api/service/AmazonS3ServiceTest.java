package com.ladbrokescoral.oxygen.cms.api.service;

import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.mockito.Mockito.*;

import com.amazonaws.services.s3.AmazonS3;
import com.ladbrokescoral.oxygen.cms.api.service.impl.AmazonS3ServiceImpl;
import com.ladbrokescoral.oxygen.cms.api.service.impl.CachePurgeService;
import java.lang.reflect.Constructor;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;

@RunWith(MockitoJUnitRunner.class)
public class AmazonS3ServiceTest {
  private final String TYPE = "s3";
  private final String BRAND = "bma";
  private final String PATH = "http://sports.coral.co.uk";
  @Mock private CachePurgeService cachePurgeService;
  @Mock private AmazonS3 amazonS3;
  @InjectMocks private AmazonS3ServiceImpl service;

  @Before
  public void init() throws Exception {
    Constructor<AmazonS3ServiceImpl> constructor =
        AmazonS3ServiceImpl.class.getDeclaredConstructor(
            AmazonS3.class, String.class, String.class, CachePurgeService.class);
    constructor.setAccessible(true);
    service = constructor.newInstance(amazonS3, TYPE, PATH, cachePurgeService);
  }

  @Test
  public void testToDeleteFile() {
    boolean result = service.deleteFile(PATH);
    assertTrue(result);
  }

  @Test
  public void testToGetMasterDataByLineItem() {
    doNothing().when(cachePurgeService).purgeCache(BRAND, PATH, "", "");
    service.purgeCache(BRAND, PATH, "", "");
    verify(cachePurgeService, times(1)).purgeCache(BRAND, PATH, "", "");
  }
}
