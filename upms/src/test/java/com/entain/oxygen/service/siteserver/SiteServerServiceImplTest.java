package com.entain.oxygen.service.siteserver;

import static org.junit.jupiter.api.Assertions.assertSame;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.anyList;
import static org.mockito.Mockito.*;

import com.egalacoral.spark.siteserver.api.*;
import com.entain.oxygen.configuration.SiteServerApiConfig;
import java.util.ArrayList;
import java.util.Optional;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;
import org.mockito.Mockito;

class SiteServerServiceImplTest {

  @Test
  void testGetHorseEvents() {
    SiteServerApiProvider siteServerApiProvider = mock(SiteServerApiProvider.class);
    SiteServerService service = new SiteServerServiceImpl(siteServerApiProvider);
    SiteServerApi siteServerApi = mock(SiteServerApi.class);
    when(siteServerApiProvider.getSiteServerApi()).thenReturn(siteServerApi);

    when(siteServerApi.getEventToOutcomeForClass(
            anyList(),
            any(SimpleFilter.class),
            any(LimitToFilter.class),
            any(LimitRecordsFilter.class),
            any(ExistsFilter.class),
            anyList()))
        .thenReturn(Optional.of(new ArrayList<>()));

    Assertions.assertNotNull(service.getHorseEvents());
  }

  @Test
  void testGetHorseEventsError() {
    SiteServerApiProvider siteServerApiProvider = mock(SiteServerApiProvider.class);
    SiteServerService service = new SiteServerServiceImpl(siteServerApiProvider);
    SiteServerApi siteServerApi = mock(SiteServerApi.class);
    when(siteServerApiProvider.getSiteServerApi()).thenReturn(siteServerApi);

    when(siteServerApi.getEventToOutcomeForClass(
            anyList(),
            any(SimpleFilter.class),
            any(LimitToFilter.class),
            any(LimitRecordsFilter.class),
            any(ExistsFilter.class),
            anyList()))
        .thenReturn(Optional.empty());

    Assertions.assertThrows(RuntimeException.class, () -> service.getHorseEvents());
  }

  @Test
  void getSiteServerApiShouldReturnConfiguredApi() {
    SiteServerApiConfig configMock = mock(SiteServerApiConfig.class);
    SiteServerApi expectedApi = mock(SiteServerApi.class);
    when(configMock.siteServerAPI()).thenReturn(expectedApi);
    SiteServerApiProviderImpl provider = new SiteServerApiProviderImpl(configMock);
    SiteServerApi resultApi = provider.getSiteServerApi();
    Mockito.verify(configMock, times(1)).siteServerAPI();
    assertSame(expectedApi, resultApi);
  }
}
