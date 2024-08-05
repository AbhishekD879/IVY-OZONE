package com.ladbrokescoral.oxygen.listeners;

import com.corundumstudio.socketio.Configuration;
import com.corundumstudio.socketio.SocketIOServer;
import com.ladbrokescoral.oxygen.model.FreebetOffer;
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.apache.kafka.common.record.TimestampType;
import org.assertj.core.api.WithAssertions;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

@ExtendWith(MockitoExtension.class)
class BetPackListenerTest implements WithAssertions {

  @Mock private SocketIOServer socketIOServer;

  @InjectMocks private BetPackListener betPackListener;

  @BeforeEach
  void setUp() {
    betPackListener = new BetPackListener(socketIOServer);
  }

  @Test
  void consumeBetPack_Success() {
    Configuration config = new Configuration();
    config.setHostname("localhost");
    config.setPort(9090);
    socketIOServer = new SocketIOServer(config);
    betPackListener = new BetPackListener(socketIOServer);
    Assertions.assertDoesNotThrow(() -> betPackListener.consumeBetPack(getConsumerRecord(true)));
  }

  @Test
  void consumeBetPack_Failure() {
    Assertions.assertDoesNotThrow(() -> betPackListener.consumeBetPack(getConsumerRecord(true)));
  }

  @Test
  void consumeBetPack_NullFreeBetObject() {
    Assertions.assertDoesNotThrow(() -> betPackListener.consumeBetPack(getConsumerRecord(false)));
  }

  public ConsumerRecord<String, FreebetOffer> getConsumerRecord(boolean isRequiredOfferObj) {
    FreebetOffer freebetOffer = null;
    if (isRequiredOfferObj) {
      freebetOffer = new FreebetOffer();
      freebetOffer.setFreebetOfferId("offer_id");
    }
    return new ConsumerRecord<>(
        "test.boards.1",
        0,
        0,
        123,
        TimestampType.NO_TIMESTAMP_TYPE,
        123,
        1,
        1,
        "someKey",
        freebetOffer);
  }
}
