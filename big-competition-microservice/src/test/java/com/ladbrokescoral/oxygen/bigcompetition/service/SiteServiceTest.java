package com.ladbrokescoral.oxygen.bigcompetition.service;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.anyBoolean;
import static org.mockito.Mockito.when;

import com.egalacoral.spark.siteserver.api.SimpleFilter;
import com.egalacoral.spark.siteserver.api.SiteServerApi;
import com.egalacoral.spark.siteserver.model.Event;
import com.ladbrokescoral.oxygen.bigcompetition.configuration.SiteServerAPIConfiguration;
import com.ladbrokescoral.oxygen.bigcompetition.service.impl.SiteServeApiServiceImpl;
import java.util.Arrays;
import java.util.List;
import java.util.Optional;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.test.util.ReflectionTestUtils;

@ExtendWith(MockitoExtension.class)
class SiteServiceTest {
  @InjectMocks SiteServeApiServiceImpl siteServeApiServiceImpl;
  @InjectMocks SiteServerAPIConfiguration siteServerAPIConfigirationTest;

  @Mock SiteServerApi siteServerApi;

  @Test
  void testSimpleFilter() {
    SimpleFilter simpleFilterForNextEventsByType =
        siteServeApiServiceImpl.getSimpleFilterForNextEventsByType();
    assertEquals("event.isStarted:isFalse", simpleFilterForNextEventsByType.getQueryMap().get(4));
  }

  @Test
  void testConfig() {
    ReflectionTestUtils.setField(siteServerAPIConfigirationTest, "isPriceBoostEnabled", false);
    ReflectionTestUtils.setField(siteServerAPIConfigirationTest, "apiVersion", "2.54");
    String version = siteServerAPIConfigirationTest.getapiVersion();
    assertEquals("2.54", version);
  }

  @Test
  void testEventToOutcomeForMarkets() {
    when(siteServerApi.getWholeEventToOutcomeForMarket(any(), anyBoolean()))
        .thenReturn(Optional.empty());
    Optional<List<Event>> events =
        siteServeApiServiceImpl.getEventToOutcomeForMarkets(Arrays.asList());
    assertFalse(events.isPresent());
  }
}
