package com.ladbrokescoral.oxygen.test.notification.client.optin;

import com.egalacoral.spark.siteserver.api.SiteServerApi;
import com.ladbrokescoral.oxygen.notification.client.optin.IGameMediaApi;
import com.ladbrokescoral.oxygen.notification.client.optin.IGameMediaApiImpl;
import java.security.KeyManagementException;
import java.security.NoSuchAlgorithmException;
import org.junit.Assert;
import org.junit.Test;

public class IGameMediaApiTest {
  @Test
  public void IGameTest() throws NoSuchAlgorithmException, KeyManagementException {
    IGameMediaApi.Builder builder = new IGameMediaApi.Builder();
    builder.setMaxNumberOfRetries(2);
    builder.setConnectionTimeout(2);
    builder.setLoggingLevel(SiteServerApi.Level.HEADERS);
    builder.setReadTimeout(2);
    builder.setUrl("https://www.abcd.com");
    IGameMediaApiImpl iGameMediaApi = new IGameMediaApiImpl(builder);
    Assert.assertNotNull(builder);
  }
}
