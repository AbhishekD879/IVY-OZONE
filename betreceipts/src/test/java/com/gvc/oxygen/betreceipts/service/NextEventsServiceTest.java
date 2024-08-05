package com.gvc.oxygen.betreceipts.service;

import com.gvc.oxygen.betreceipts.config.NextRaceProps;
import com.gvc.oxygen.betreceipts.service.siteserve.SiteServeService;
import java.util.Arrays;
import org.assertj.core.api.WithAssertions;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.Spy;
import org.mockito.junit.jupiter.MockitoExtension;

@ExtendWith(MockitoExtension.class)
class NextEventsServiceTest implements WithAssertions {

  @Spy private NextRaceProps nextRaceProps;

  @Mock private SiteServeService siteServeService;

  @InjectMocks private NextEventsService nextEventsService;

  @Test
  void testGetNextEvents() {
    Assertions.assertDoesNotThrow(() -> nextEventsService.getNextEvents());
  }

  @Test
  void testGetNextEventsWithClassesNonEmpty() {
    Mockito.when(siteServeService.getActiveClassesForCategoryId(Mockito.anyInt()))
        .thenReturn(Arrays.asList("1", "2"));
    Assertions.assertDoesNotThrow(() -> nextEventsService.getNextEvents());
  }
}
