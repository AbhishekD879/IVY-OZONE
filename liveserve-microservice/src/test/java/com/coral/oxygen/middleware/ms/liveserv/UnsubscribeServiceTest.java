package com.coral.oxygen.middleware.ms.liveserv;

import com.coral.oxygen.middleware.ms.liveserv.exceptions.ServiceException;
import com.coral.oxygen.middleware.ms.liveserv.model.SubscriptionStats;
import com.coral.oxygen.middleware.ms.liveserv.model.SubscriptionStatsOld;
import com.coral.siteserver.api.SiteServerService;
import java.util.*;
import org.junit.After;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.junit.MockitoJUnitRunner;
import org.springframework.context.ApplicationEventPublisher;

/** Created by ogavur on 5/16/17. */
@RunWith(MockitoJUnitRunner.class)
public class UnsubscribeServiceTest {

  @Mock LiveServService liveServService;
  @Mock SiteServerService siteServerService;
  @Mock ApplicationEventPublisher applicationEventPublisher;

  @InjectMocks private UnsubscribeService service;

  @Before
  public void setUp() throws ServiceException {
    Map<String, SubscriptionStats> subscMap = new HashMap<>();
    subscMap.put("1", new SubscriptionStatsOld("sEVENT0000000001", 1));
    subscMap.put("2", new SubscriptionStatsOld("sEVENT0000000002", 2));
    subscMap.put("6", new SubscriptionStatsOld("sSELCN0000000006", 2));
    subscMap.put("7", new SubscriptionStatsOld("sEVMKT0000000007", 2));
    subscMap.put("3", new SubscriptionStatsOld("sEVENT0000000003", 3));
    Mockito.when(liveServService.getSubscriptions()).thenReturn(subscMap);
    List<Long> activeEventsIds = new ArrayList<>();
    activeEventsIds.add(1L);
    Mockito.when(siteServerService.getEventIdS(Arrays.asList(1L, 2L, 3L)))
        .thenReturn(activeEventsIds);
  }

  @After
  public void tearDown() {
    service = null;
  }

  @Test
  public void testUnsubscribeScheduler() {
    service.unSubscribe();
    Mockito.verify(applicationEventPublisher, Mockito.times(0))
        .publishEvent(new ChannelUnsubcribeEvent(service, "sEVENT0000000001"));
    Mockito.verify(applicationEventPublisher)
        .publishEvent(new ChannelUnsubcribeEvent(service, "sEVENT0000000002"));
    Mockito.verify(applicationEventPublisher)
        .publishEvent(new ChannelUnsubcribeEvent(service, "sSELCN0000000006"));
    Mockito.verify(applicationEventPublisher)
        .publishEvent(new ChannelUnsubcribeEvent(service, "sEVMKT0000000007"));
    Mockito.verify(applicationEventPublisher)
        .publishEvent(new ChannelUnsubcribeEvent(service, "sEVENT0000000003"));
    liveServService.getSubscriptions();
  }
}
