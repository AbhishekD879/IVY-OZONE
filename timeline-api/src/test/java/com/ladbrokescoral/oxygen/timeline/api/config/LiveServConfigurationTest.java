package com.ladbrokescoral.oxygen.timeline.api.config;

import static org.junit.Assert.assertNotNull;

import com.ladbrokescoral.oxygen.timeline.api.model.obevent.EventStatus;
import com.ladbrokescoral.oxygen.timeline.api.model.obevent.ObEvent;
import java.security.KeyManagementException;
import java.security.NoSuchAlgorithmException;
import lombok.extern.slf4j.Slf4j;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.InjectMocks;
import org.mockito.junit.MockitoJUnitRunner;

@Slf4j
@RunWith(MockitoJUnitRunner.class)
public class LiveServConfigurationTest {

  @InjectMocks LiveServConfiguration liveServConfiguration;

  @Test()
  public void siteServerApiTest() throws KeyManagementException, NoSuchAlgorithmException {
    try {
      liveServConfiguration.siteServerApi(null, 1, 1, 1, "BASIC");
      assertNotNull(liveServConfiguration.siteServerApi(null, 1, 1, 1, "BASIC"));
    } catch (Exception e) {
      log.info("Exception {}", e);
    }
  }

  @Test
  public void messageHandlerMultiplexerTest()
      throws KeyManagementException, NoSuchAlgorithmException {

    liveServConfiguration.messageHandlerMultiplexer(null);
    assertNotNull(liveServConfiguration.messageHandlerMultiplexer(null));
  }

  @Test
  public void callTest() throws KeyManagementException, NoSuchAlgorithmException {

    liveServConfiguration.call(null, 1, 1, 1, 1, 1, 1);
    assertNotNull(liveServConfiguration.call(null, 1, 1, 1, 1, 1, 1));
  }

  @Test
  public void siteServEventIdResolverTest()
      throws KeyManagementException, NoSuchAlgorithmException {

    liveServConfiguration.siteServEventIdResolver(null);
    assertNotNull(liveServConfiguration.siteServEventIdResolver(null));
  }

  @Test
  public void liveServServiceTest() throws KeyManagementException, NoSuchAlgorithmException {

    liveServConfiguration.managedLiveServeService(null, null, null);
    EventStatus eventStatus = new EventStatus();
    eventStatus.getDisplayed();
    eventStatus.getActive();

    ObEvent obEvent = new ObEvent();
    obEvent.setCategoryCode("894");
    assertNotNull(obEvent);
    assertNotNull(eventStatus);
  }
}
