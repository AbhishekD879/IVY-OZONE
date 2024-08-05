package com.ladbrokescoral.oxygen.listeners;

import static org.mockito.Mockito.times;
import static org.mockito.Mockito.verify;

import com.corundumstudio.socketio.AckRequest;
import com.corundumstudio.socketio.SocketIOClient;
import com.ladbrokescoral.oxygen.listeners.showdown.LeaderBoardListener;
import com.ladbrokescoral.oxygen.service.KafkaPublisherImpl;
import com.ladbrokescoral.oxygen.service.LeaderboardReqPublisher;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.kafka.core.KafkaTemplate;

@ExtendWith(MockitoExtension.class)
class LeaderBoardListenerTest {

  @Mock private LeaderboardReqPublisher leaderboardReqPublisher;
  @InjectMocks private LeaderBoardListener listener;
  @Mock SocketIOClient socketClient;
  @Mock KafkaTemplate<String, String> kafkaTemplate;
  @Mock private KafkaPublisherImpl kafkaPublisherImpl;

  @Test
  void onDataTest() throws Exception {
    String data = "Leaderboard::12345";
    AckRequest ackSender = null;
    listener.onData(socketClient, data, ackSender);
    verify(leaderboardReqPublisher, times(1)).publish(Mockito.any(), Mockito.any());
  }
}
