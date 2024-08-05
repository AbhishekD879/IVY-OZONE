package com.ladbrokescoral.oxygen.listeners.betpack;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.*;

import com.corundumstudio.socketio.AckRequest;
import com.corundumstudio.socketio.HandshakeData;
import com.corundumstudio.socketio.SocketIOClient;
import com.ladbrokescoral.oxygen.dto.messages.BetPackMessage;
import com.ladbrokescoral.oxygen.listeners.ThrottleLogic;
import com.ladbrokescoral.oxygen.model.*;
import com.ladbrokescoral.oxygen.service.BetPackKafkaPublisher;
import com.ladbrokescoral.oxygen.service.betpack.BetPackRedisOperations;
import java.util.*;
import java.util.concurrent.CompletableFuture;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.junit.jupiter.MockitoExtension;

@ExtendWith(MockitoExtension.class)
class SubscribeBetPackListenerTest {

  @Mock private BetPackKafkaPublisher betPackKafkaPublisher;
  @Mock private BetPackRedisOperations betPackRedisOperations;
  private SubscribeBetPackListener listener;
  @Mock SocketIOClient socketClient;
  @Mock private ThrottleLogic throttleLogic;
  private final String CHANNEL = "redis_operations _channel";

  @Mock HandshakeData handshakeData;

  @BeforeEach
  public void init() {
    listener =
        new SubscribeBetPackListener(betPackKafkaPublisher, betPackRedisOperations, throttleLogic);
  }

  @Test
  void onDataTest() {
    List<String> data = new ArrayList<>();
    data.add("1233");
    AckRequest ackSender = null;
    when(throttleLogic.hackerDetected(Mockito.any(), Mockito.any())).thenReturn(true);
    listener.onData(socketClient, data, ackSender);
    verify(betPackKafkaPublisher, times(0)).publish(any(), any());
  }

  @Test
  void onDataTestIsChannelOpenTestFalse() {
    List<String> data = new ArrayList<>();
    data.add("1,2,3");
    AckRequest ackSender = null;
    Set<String> set = new HashSet<String>();
    set.add("c::1233");
    when(throttleLogic.hackerDetected(Mockito.any(), Mockito.any())).thenReturn(false);
    when(socketClient.getHandshakeData()).thenReturn(handshakeData);
    listener.onData(socketClient, data, ackSender);
    assertNotNull(data);
  }

  @Test
  void onDataTestIsChannelOpenTest() throws Exception {
    List<String> data = new ArrayList<>();
    data.add("1");
    FreebetOffer freebetOffer = new FreebetOffer();
    freebetOffer.setFreebetOfferId("1");
    BetPackMessage message = new BetPackMessage();
    AckRequest ackSender = null;
    Set<String> set = new HashSet<String>();
    set.add("c::1233");
    when(throttleLogic.hackerDetected(Mockito.any(), Mockito.any())).thenReturn(false);
    when(socketClient.isChannelOpen()).thenReturn(true);
    when(betPackRedisOperations.getLastMessage(anyString()))
        .thenReturn(CompletableFuture.completedFuture(Optional.empty()));
    when(socketClient.getSessionId()).thenReturn(new UUID(1234, 0));
    when(socketClient.getAllRooms()).thenReturn(set);
    listener.onData(socketClient, data, ackSender);
    assertNotNull(data);
  }

  @Test
  void onDataTestIsChannelOpenTestWithData() throws Exception {
    List<String> data = new ArrayList<>();
    data.add("1");
    FreebetOffer freebetOffer = new FreebetOffer();
    freebetOffer.setFreebetOfferId("1");
    BetPackMessage message = new BetPackMessage();
    message.setBetPackId("1");

    FreebetTriggerAmount freebetTriggerAmount = new FreebetTriggerAmount();
    freebetTriggerAmount.setCurrency("USD");
    freebetTriggerAmount.setValue("10");
    FreebetTrigger freebetTrigger = new FreebetTrigger();
    freebetTrigger.setFreebetTriggerAmount(freebetTriggerAmount);
    freebetTrigger.setFreebetTriggerBonus("bonus");
    freebetTrigger.setFreebetTriggerId("1");
    freebetTrigger.setFreebetTriggerBetType("type");
    freebetTrigger.setFreebetTriggerMaxBonus("bonus");
    freebetTrigger.setFreebetTriggerBonus("bonus");
    freebetTrigger.setFreebetTriggerMaxLoseLegs("legs");
    freebetTrigger.setFreebetTriggerCalcMethod("calcMethod");
    freebetTrigger.setFreebetTriggerMinLegPriceDen("1");
    freebetTrigger.setFreebetTriggerQualification("qual");
    freebetTrigger.setFreebetTriggerMinPriceNum("1");
    freebetTrigger.setFreebetTriggerType("type");
    freebetTrigger.setFreebetTriggerRank("1");
    freebetTrigger.setFreebetTriggerMinLegPriceNum("num");
    freebetTrigger.setFreebetTriggerMinPriceDen("1");
    freebetTrigger.setFreebetTriggerMinLegPriceNum("1");
    freebetTrigger.setFreebetTriggerMaxLoseLegs("loose");
    freebetTrigger.setFreebetTriggerPrecentageBonus("bonus");
    freebetTrigger.setFreebetTriggerMinLoseLegs("legs");

    freebetOffer.setFreebetOfferName("name");
    freebetOffer.setFreebetOfferId("1");
    freebetOffer.setDescription("desc");
    freebetOffer.setEndTime("end");
    freebetOffer.setFreebetOfferCcyCodes("ccy");
    freebetOffer.setStartTime("start");
    freebetOffer.setStatus("A");

    FreebetOfferLimits freebetOfferLimits = new FreebetOfferLimits();
    LimitEntry limitEntry = new LimitEntry();
    LimitDefinition limitDefinition = new LimitDefinition();
    LimitComponent limitComponent = new LimitComponent();
    LimitParam limitParam = new LimitParam();
    limitParam.setValue(1);
    limitParam.setName("name");

    limitComponent.setLimitParam(Arrays.asList(limitParam));

    limitDefinition.setLimitComponent(limitComponent);

    limitEntry.setLimitDefinition(limitDefinition);
    limitEntry.setLimitId(1);
    limitEntry.setLimitRemaining("1");
    limitEntry.setLimitSort("1");
    // freebetOfferLimits.setLimitEntry(limitEntry);

    freebetOffer.setFreebetOfferLimits(freebetOfferLimits);
    freebetOffer.setFreebetTrigger(Arrays.asList(freebetTrigger));
    FreebetToken freebetToken = new FreebetToken();
    freebetToken.setFreebetTokenId("1");
    freebetToken.setFreebetTokenDisplayText("text");
    FreebetTokenValue freebetTokenValue = new FreebetTokenValue();
    freebetTokenValue.setValue("10");
    freebetTokenValue.setCurrency("ccy");
    freebetToken.setFreebetTokenValue(Arrays.asList(freebetTokenValue));
    freebetOffer.setFreebetToken(Arrays.asList(freebetToken));
    message.setMessage(freebetOffer);

    AckRequest ackSender = null;
    Set<String> set = new HashSet<String>();
    set.add("c::1233");
    when(throttleLogic.hackerDetected(Mockito.any(), Mockito.any())).thenReturn(false);
    when(socketClient.isChannelOpen()).thenReturn(true);
    when(betPackRedisOperations.getLastMessage(anyString()))
        .thenReturn(
            CompletableFuture.completedFuture(
                Optional.of(new BetPackMessage(CHANNEL, freebetOffer))));
    when(socketClient.getSessionId()).thenReturn(new UUID(1234, 0));
    when(socketClient.getAllRooms()).thenReturn(set);
    listener.onData(socketClient, data, ackSender);
    assertNotNull(data);
    assertNotNull(message);
    assertNotNull(message.getMessage());
    assertNotNull(message.getMessage().getFreebetTrigger());
    assertNotNull(message.getMessage().getFreebetToken());
    assertNotNull(message.getMessage().getFreebetOfferLimits());
    // assertNotNull(message.getMessage().getFreebetOfferLimits().getLimitEntry());

    assertThat(message.getBetPackId()).isEqualTo("1");
    assertThat(message.getMessage().getFreebetTrigger().get(0).getFreebetTriggerAmount().getValue())
        .isBetween("1", "100");
    assertThat(
            message.getMessage().getFreebetTrigger().get(0).getFreebetTriggerAmount().getCurrency())
        .isNotNull();
    assertThat(message.getMessage().getFreebetTrigger().get(0))
        .hasFieldOrProperty("freebetTriggerId");
    assertThat(message.getMessage().getFreebetTrigger().get(0)).hasNoNullFieldsOrProperties();
    // assertThat(message.getMessage()).hasNoNullFieldsOrProperties();
    // assertThat(message.getMessage().getFreebetToken()).hasNoNullFieldsOrProperties();
    assertThat(message.getMessage().getFreebetToken().get(0).getFreebetTokenId()).isNotNull();
    assertThat(message.getMessage().getFreebetToken().get(0).getFreebetTokenDisplayText())
        .isNotNull();
    assertNotNull(message.getMessage().getFreebetToken().get(0).getFreebetTokenValue());
    assertThat(message.getMessage().getFreebetToken().get(0).getFreebetTokenValue().get(0))
        .hasNoNullFieldsOrProperties();
    /*
    assertThat(message.getMessage().getFreebetOfferLimits().getLimitEntry())
        .hasNoNullFieldsOrProperties();

    assertThat(message.getMessage().getFreebetOfferLimits().getLimitEntry().getLimitDefinition())
        .hasNoNullFieldsOrProperties();
    assertThat(
            message
                .getMessage()
                .getFreebetOfferLimits()
                .getLimitEntry()
                .getLimitDefinition()
                .getLimitComponent())
        .hasNoNullFieldsOrProperties();
    assertThat(
            message
                .getMessage()
                .getFreebetOfferLimits()
                .getLimitEntry()
                .getLimitDefinition()
                .getLimitComponent()
                .getLimitParam()
                .get(0))
        .hasNoNullFieldsOrProperties();
    assertThat(
            message
                .getMessage()
                .getFreebetOfferLimits()
                .getLimitEntry()
                .getLimitDefinition()
                .getLimitComponent()
                .getLimitParam()
                .get(0)
                .getValue())
        .isEqualTo(1);
    assertThat(
            message
                .getMessage()
                .getFreebetOfferLimits()
                .getLimitEntry()
                .getLimitDefinition()
                .getLimitComponent()
                .getLimitParam()
                .get(0)
                .getName())
        .isEqualTo("name");

     */
  }

  @Test
  void onDataTestIsChannelOpenTestWithDataBtePackNull() throws Exception {
    List<String> data = new ArrayList<>();
    data.add("2");
    FreebetOffer freebetOffer = new FreebetOffer();
    freebetOffer.setFreebetOfferId("1");
    BetPackMessage message = new BetPackMessage();
    AckRequest ackSender = null;
    Set<String> set = new HashSet<String>();
    set.add("2");
    when(throttleLogic.hackerDetected(Mockito.any(), Mockito.any())).thenReturn(false);
    when(socketClient.isChannelOpen()).thenReturn(true);
    when(betPackRedisOperations.getLastMessage(anyString()))
        .thenReturn(
            CompletableFuture.completedFuture(
                Optional.of(new BetPackMessage(CHANNEL, freebetOffer))));
    when(socketClient.getSessionId()).thenReturn(new UUID(1234, 0));
    when(socketClient.getAllRooms()).thenReturn(set);
    listener.onData(socketClient, data, ackSender);
    assertNotNull(data);
  }

  @Test
  void onDataTestIsChannelOpenTestWithDataBtePackNullAndInCache() throws Exception {
    List<String> data = new ArrayList<>();
    data.add("2");
    FreebetOffer freebetOffer = new FreebetOffer();
    freebetOffer.setFreebetOfferId("1");
    BetPackMessage message = new BetPackMessage();
    AckRequest ackSender = null;
    Set<String> set = new HashSet<String>();
    set.add("2");
    when(throttleLogic.hackerDetected(Mockito.any(), Mockito.any())).thenReturn(false);
    when(socketClient.isChannelOpen()).thenReturn(true);
    when(betPackRedisOperations.getLastMessage(anyString()))
        .thenReturn(
            CompletableFuture.completedFuture(
                Optional.of(new BetPackMessage(CHANNEL, freebetOffer))));
    when(socketClient.getSessionId()).thenReturn(new UUID(1234, 0));
    when(socketClient.getAllRooms()).thenReturn(set);
    listener.onData(socketClient, data, ackSender);
    assertNotNull(data);
  }

  @Test
  void TestOfferGroup() {
    OfferGroup offerGroup = new OfferGroup();
    offerGroup.setOfferGroupId("1");
    offerGroup.setOfferGroupName("test");
    assertEquals("1", offerGroup.getOfferGroupId());
    assertEquals("test", offerGroup.getOfferGroupName());
  }
}
