package com.ladbrokescoral.cashout.config;

import static org.mockito.Mockito.times;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

import com.corundumstudio.socketio.BroadcastOperations;
import com.corundumstudio.socketio.SocketIOServer;
import com.ladbrokescoral.cashout.payout.PotentialReturns;
import java.util.ArrayList;
import java.util.List;
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.apache.kafka.common.header.Header;
import org.apache.kafka.common.header.Headers;
import org.apache.kafka.common.header.internals.RecordHeaders;
import org.apache.kafka.common.record.TimestampType;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.junit.jupiter.MockitoExtension;
import org.mockito.junit.jupiter.MockitoSettings;
import org.mockito.quality.Strictness;

@ExtendWith(MockitoExtension.class)
@MockitoSettings(strictness = Strictness.LENIENT)
class InternalKafkaMessageListenerTest {
  @InjectMocks InternalKafkaMessageListener internalKafkaMessageListener;
  @Mock private SocketIOServer socketIOServer;
  @Mock private BroadcastOperations broadcastOperations;

  @Test
  void triggerBetDetailsRequestTest() {
    List<Header> headers = new ArrayList<>();
    Headers header = new RecordHeaders(headers);
    ConsumerRecord<String, Object> record =
        new ConsumerRecord<>(
            "bet-detail-requests",
            0,
            0,
            123,
            TimestampType.NO_TIMESTAMP_TYPE,
            123L,
            1,
            1,
            "bet-detail-requests",
            createPayoutResponse(),
            header);
    when(socketIOServer.getRoomOperations(record.key())).thenReturn(broadcastOperations);
    internalKafkaMessageListener.onPayoutUpdate(record);
    internalKafkaMessageListener.onEventUpdate(record);
    internalKafkaMessageListener.onTwoUpUpdate(record);
    verify(socketIOServer, times(3)).getRoomOperations(Mockito.any());
  }

  private Object createPayoutResponse() {
    PotentialReturns potentialReturns = new PotentialReturns();
    potentialReturns.setBetId("22198739");
    potentialReturns.setReturns(0.0);
    return potentialReturns;
  }
}
