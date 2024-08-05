package com.ladbrokescoral.oxygen.listeners;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.times;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

import com.corundumstudio.socketio.AckRequest;
import com.corundumstudio.socketio.SocketIOClient;
import com.ladbrokescoral.oxygen.listeners.showdown.UnsubscribeShowdownListener;
import com.ladbrokescoral.oxygen.service.KafkaPublisherImpl;
import com.ladbrokescoral.oxygen.service.LeaderboardReqPublisher;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;
import java.util.UUID;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.kafka.core.KafkaTemplate;

@ExtendWith(MockitoExtension.class)
class UnsubscribeShowdownListenerTest {
  @Mock private LeaderboardReqPublisher leaderboardReqPublisher;
  private static final String TOPIC = "topic";
  private UnsubscribeShowdownListener listener;
  @Mock SocketIOClient socketClient;
  @Mock KafkaTemplate<String, String> kafkaTemplate;
  @Mock private KafkaPublisherImpl kafkaPublisherImpl;

  @BeforeEach
  public void init() {
    listener = new UnsubscribeShowdownListener(leaderboardReqPublisher);
  }

  @Test
  void onDataTest() throws Exception {
    List<String> data = new ArrayList<>();
    data.add("c::1233");
    AckRequest ackSender = null;
    Set<String> set = new HashSet<String>();
    set.add("c::1233");
    when(socketClient.getSessionId()).thenReturn(new UUID(1234, 0));
    when(socketClient.getAllRooms()).thenReturn(set);
    listener.onData(socketClient, data, ackSender);
    verify(leaderboardReqPublisher, times(1)).publish(any(), any());
  }

  @Test
  void onDataTest1() throws Exception {
    List<String> data = new ArrayList<>();
    data.add("ENTRY_INFO::2562909748");
    data.add("LDRBRD::60c38852f5860a2012497c3d::Dachanta::12345");
    data.add("MYENTRIES::60c38852f5860a2012497c3d::Dachanta::0");
    data.add("MYENTRIES::60c38852f5860a2012497c3d::Dachanta");
    data.add("LDRBRD::60c38852f5860a2012497c3d::Dachanta");
    data.add("EVENT::1234566778");
    data.add("SCORE::1234566778");
    data.add("CLOCK::1234566778");
    AckRequest ackSender = null;
    Set<String> set = new HashSet<String>();
    set.add("c::1233");
    when(socketClient.getSessionId()).thenReturn(new UUID(1234, 0));
    when(socketClient.getAllRooms()).thenReturn(set);
    listener.onData(socketClient, data, ackSender);
    verify(leaderboardReqPublisher, times(8)).publish(any(), any());
  }
}
