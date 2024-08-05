package com.gvc.oxygen.betreceipts.liveserv;

import com.coral.oxygen.middleware.ms.liveserv.LiveServService;
import com.coral.oxygen.middleware.ms.liveserv.client.model.Message;
import com.coral.oxygen.middleware.ms.liveserv.model.messages.MessageEnvelope;
import com.egalacoral.spark.siteserver.model.Children;
import com.egalacoral.spark.siteserver.model.Market;
import com.egalacoral.spark.siteserver.model.Outcome;
import com.egalacoral.spark.siteserver.model.Price;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.google.gson.Gson;
import com.gvc.oxygen.betreceipts.entity.NextRace;
import com.gvc.oxygen.betreceipts.entity.NextRaceMap;
import com.gvc.oxygen.betreceipts.liveserv.updates.SelectionMessageApplier;
import com.gvc.oxygen.betreceipts.service.EventService;
import java.util.Arrays;
import java.util.List;
import java.util.Optional;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.Spy;
import org.mockito.junit.jupiter.MockitoExtension;

@ExtendWith(MockitoExtension.class)
class SelectionMessageApplierTest {

  @Mock private LiveServService liveServService;

  @Mock private EventService eventService;

  @Spy private ObjectMapper objectMapper;

  @InjectMocks private SelectionMessageApplier selectionMessageApplier;

  @Test
  void testHandleWithMessage() {
    MessageEnvelope messageEnvelope = getMessageEnvelope();
    Assertions.assertDoesNotThrow(() -> selectionMessageApplier.applyUpdate(messageEnvelope));
  }

  @Test
  void testHandleWithMessageForNextRace() {
    MessageEnvelope messageEnvelope = getMessageEnvelope();
    Mockito.when(eventService.getNextRaceMapById(Mockito.anyString()))
        .thenReturn(Optional.of(getNextRaceMap("sEVENT993420000")));
    Assertions.assertDoesNotThrow(() -> selectionMessageApplier.applyUpdate(messageEnvelope));
  }

  @Test
  void testHandleWithMessageForNextRaceWithSameSelection() {
    MessageEnvelope messageEnvelope = getMessageEnvelope();
    Mockito.when(eventService.getNextRaceMapById(Mockito.anyString()))
        .thenReturn(Optional.of(getNextRaceMap("dafdfdf")));
    Assertions.assertDoesNotThrow(() -> selectionMessageApplier.applyUpdate(messageEnvelope));
  }

  @Test
  void testHandleWithMessageForNextRaceForException() {
    MessageEnvelope messageEnvelope = getMessageEnvelope();
    Mockito.when(eventService.getNextRaceMapById(Mockito.anyString()))
        .thenThrow(new IllegalArgumentException());
    Assertions.assertDoesNotThrow(() -> selectionMessageApplier.applyUpdate(messageEnvelope));
  }

  @Test
  void testHandleWithMessageForException() {
    MessageEnvelope messageEnvelope = getMessageEnvelope();
    messageEnvelope.getMessage().setJsonData(getMessageInvalid());
    Assertions.assertDoesNotThrow(() -> selectionMessageApplier.applyUpdate(messageEnvelope));
  }

  private MessageEnvelope getMessageEnvelope() {
    return new MessageEnvelope("sEVENT993420000", 2233445, getMessage());
  }

  private Message getMessage() {
    Message message = new Message();
    message.setMessageCode("code1");
    message.setJsonData(
        "{\"status\":\"A\",\"displayed\":\"Y\",\"settled\":\"Y\",\"lp_num\":\"7\",\"lp_den\":\"9\"}");
    return message;
  }

  private NextRaceMap getNextRaceMap(String outcome) {

    return new NextRaceMap("2", new Gson().toJson(getNextRace(outcome)), 1);
  }

  private NextRace getNextRace(String outcome) {
    NextRace nextRace = new NextRace();
    nextRace.setMarkets(Arrays.asList(getMarkets("win or eachway", outcome)));
    return nextRace;
  }

  private String getMessageInvalid() {
    return "{\"status\":\"A\",\"displayed\":\"Y\",\"result_conf\":\"Y\",\"started\":\"Y\"";
  }

  private Market getMarkets(String name, String outcome) {
    Market market = new Market();
    market.setChildren(getOutcomes(name, outcome));
    return market;
  }

  private List<Children> getOutcomes(String name, String outcome) {
    Children children = new Children();
    children.setOutcome(getOutcome(name, outcome));
    return Arrays.asList(children);
  }

  private Outcome getOutcome(String name, String channel) {
    Outcome outcome = new Outcome();
    outcome.setName(name);
    outcome.setLiveServChannels(channel);
    outcome.setChildren(Arrays.asList(getPriceChildern()));
    return outcome;
  }

  private Children getPriceChildern() {
    Children children = new Children();
    children.setPrice(new Price());
    return children;
  }
}
