package com.coral.oxygen.cms.api.impl;

import static org.junit.Assert.*;

import okhttp3.OkHttpClient;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.junit.MockitoJUnitRunner;

@RunWith(MockitoJUnitRunner.class)
public class CmsServiceImplTest {

  @Test(expected = IllegalArgumentException.class)
  public void requestPages_Url_Fail() {
    CmsServiceImpl cmsService = new CmsServiceImpl("test", new OkHttpClient());
    assertNotNull(cmsService);
  }
}
