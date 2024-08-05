package com.gvc.oxygen.betreceipts.liveserv;

import com.coral.oxygen.middleware.ms.liveserv.LiveServService;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.gvc.oxygen.betreceipts.liveserv.updates.ChannelMessageApplier;
import com.gvc.oxygen.betreceipts.liveserv.updates.EventMessageApplier;
import com.gvc.oxygen.betreceipts.liveserv.updates.LiveserveMessageApplierFactory;
import com.gvc.oxygen.betreceipts.liveserv.updates.SelectionMessageApplier;
import com.gvc.oxygen.betreceipts.service.EventService;
import java.util.ArrayList;
import java.util.List;
import java.util.stream.Stream;
import org.assertj.core.api.WithAssertions;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.junit.jupiter.MockitoExtension;

@ExtendWith(MockitoExtension.class)
class LiveMessageApplierFactoryTest implements WithAssertions {
  @Mock private List<ChannelMessageApplier> channelMessageApplier;

  @Mock private ObjectMapper objectMapper;

  @Mock private LiveServService liveServService;

  @Mock private EventService eventService;

  @InjectMocks private LiveserveMessageApplierFactory liveserveMessageApplierFactory;

  @Test
  void testHandleWithMessage() {
    Mockito.when(channelMessageApplier.stream()).thenReturn(getChannelMessageApplier());
    Assertions.assertDoesNotThrow(() -> liveserveMessageApplierFactory.get("sEVENT3445445"));
  }

  @Test
  void testHandleWithMessageForException() throws IllegalStateException {
    Mockito.when(channelMessageApplier.stream()).thenReturn(getChannelMessageApplier());

    IllegalArgumentException ex =
        Assertions.assertThrows(
            IllegalArgumentException.class,
            () -> liveserveMessageApplierFactory.get("sOut3445445"));
    assertThat(ex)
        .isInstanceOf(IllegalArgumentException.class)
        .hasMessage("No defined message applier for channel: sOut3445445");
  }

  private Stream<ChannelMessageApplier> getChannelMessageApplier() {
    EventMessageApplier eventMessageApplier =
        new EventMessageApplier(objectMapper, eventService, liveServService);

    SelectionMessageApplier selectionMessageApplier =
        new SelectionMessageApplier(objectMapper, eventService, liveServService);

    List<ChannelMessageApplier> list = new ArrayList<>();
    list.add(eventMessageApplier);
    list.add(selectionMessageApplier);
    return list.stream();
  }
}
