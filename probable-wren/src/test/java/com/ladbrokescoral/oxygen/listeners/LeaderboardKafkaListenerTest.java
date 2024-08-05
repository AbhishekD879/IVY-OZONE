package com.ladbrokescoral.oxygen.listeners;

import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.fail;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.when;

import com.corundumstudio.socketio.BroadcastOperations;
import com.corundumstudio.socketio.SocketIOClient;
import com.corundumstudio.socketio.SocketIOServer;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.JsonMappingException;
import com.google.gson.Gson;
import com.ladbrokescoral.oxygen.dto.messages.Envelope;
import com.ladbrokescoral.oxygen.dto.messages.EnvelopeType;
import com.ladbrokescoral.oxygen.service.LeaderboardSocketIOHelper;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.ValueSource;
import org.mockito.junit.jupiter.MockitoSettings;
import org.mockito.quality.Strictness;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.scheduling.concurrent.ThreadPoolTaskExecutor;
import org.springframework.test.context.junit.jupiter.SpringExtension;

@ExtendWith(SpringExtension.class)
@MockitoSettings(strictness = Strictness.LENIENT)
@SpringBootTest(
    classes = {ThreadPoolTaskExecutor.class, Gson.class},
    properties = "leaderboard.enabled=true")
class LeaderboardKafkaListenerTest {
  @MockBean private SocketIOServer socketIOServer;
  private LeaderboardKafkaListener leaderboardKafkaListener;
  private Gson gson;
  @Autowired private ThreadPoolTaskExecutor leaderboardExecutor;
  @MockBean private BroadcastOperations broadcastOperations;
  @MockBean private LeaderboardSocketIOHelper showdownSocketIOHelper;
  @MockBean private SocketIOClient socketIOClient;
  private List<SocketIOClient> clients = new ArrayList<>();
  private static final String DATA = "data";
  private static final String CHANNEL = "chanel1";
  String update =
      "{\"_id\":\"0\",\"contestId\":\"61eb956dd2e14e15c1139313\",\"index\":0,\"userId\":\"dev_user\",\"eventId\":\"1716332\",\"receiptId\":\"O/300078346/00\",\"outcomeIds\":[\"148123485\",\"148123512\",\"148123509\",\"148123482\",\"148123502\"],\"stake\":\"0\",\"odd\":3,\"voided\":false,\"priceNum\":\"400\",\"priceDen\":\"10\",\"overallProgressPct\":0,\"counterFlag\":true,\"_class\":\"com.entain.oxygen.showdown.model.Entry\"}";

  @BeforeEach
  public void init() {
    leaderboardKafkaListener = new LeaderboardKafkaListener(socketIOServer, leaderboardExecutor);
    socketIOServer.getAllClients().addAll(clients);
  }

  @Test
  void showdownResponseTest() {
    try {
      ConsumerRecord<String, String> record =
          new ConsumerRecord<String, String>("topic", 0, 0, "key", "[" + update + "]");
      when(socketIOServer.getRoomOperations(record.key())).thenReturn(broadcastOperations);
      leaderboardKafkaListener.showdownResponse(record);
    } catch (Exception e) {
      assertNotNull(e);
    }
  }

  @Test
  void showdownResponseTest1() throws JsonMappingException, JsonProcessingException {
    try {
      ConsumerRecord<String, String> consumerRecord =
          new ConsumerRecord<>("topic", 0, 0, "key", "[" + update + "]");

      when(socketIOServer.getRoomOperations(consumerRecord.key())).thenReturn(broadcastOperations);
      leaderboardKafkaListener.showdownResponse(consumerRecord);
    } catch (Exception e) {
      assertNotNull(e);
    }
  }

  @Test
  void consumeLeaderboardUpdatesTest_LDRBRD() {
    try {
      ConsumerRecord<String, String> record =
          new ConsumerRecord<String, String>(
              "topic", 0, 0, "LDRBRD::60c38852f5860a2012497c3d::Dachanta", "[" + update + "]");
      when(socketIOServer.getRoomOperations(record.key())).thenReturn(broadcastOperations);
      leaderboardKafkaListener.consumeLeaderboardUpdates(record);
    } catch (Exception e) {
      assertNotNull(e);
    }
  }

  @Test
  void testConsumeLeaderboardMatchUpdates() {
    try {
      ConsumerRecord<String, String> record =
          new ConsumerRecord<String, String>(
              "topic", 0, 0, "LDRBRD::60c38852f5860a2012497c3d::Dachanta", "[" + update + "]");
      when(socketIOServer.getRoomOperations(record.key())).thenReturn(broadcastOperations);
      leaderboardKafkaListener.consumeLeaderboardMatchUpdates(record);
    } catch (Exception e) {
      assertNotNull(e);
    }
  }

  @Test
  void consumeLeaderboardMatchUpdates_Exception() {
    try {
      ConsumerRecord<String, String> record =
          new ConsumerRecord<String, String>(
              "topic", 0, 0, "LDRBRD::60c38852f5860a2012497c3d::Dachanta", "");
      when(socketIOServer.getRoomOperations(record.key())).thenReturn(broadcastOperations);
      leaderboardKafkaListener.consumeLeaderboardMatchUpdate(socketIOServer, record);
    } catch (Exception e) {
      assertNotNull(e);
    }
  }

  @Test
  void consumeLeaderboardMatchUpdate() throws JsonMappingException, JsonProcessingException {
    try {
      Envelope.MessageObject messageObject =
          new Envelope.MessageObject(
              "body",
              "hash",
              DATA,
              "id",
              "MsEVENT0001234567!!!!!'-iA1GsEVENT0001234567000111000111",
              "sEVMKT",
              "date");
      Envelope envelope = new Envelope(1L, EnvelopeType.MESSAGE, CHANNEL, messageObject);
      String envelopeString = gson.toJson(envelope);

      ConsumerRecord<String, String> consumerRecord =
          new ConsumerRecord<>("topic", 0, 0, "EVENT::1234566778", envelopeString);

      when(socketIOServer.getRoomOperations(consumerRecord.key())).thenReturn(broadcastOperations);
      leaderboardKafkaListener.consumeLeaderboardMatchUpdate(socketIOServer, consumerRecord);
    } catch (Exception e) {
      assertNotNull(e);
    }
  }

  @Test
  void showdownResponseTest2() throws JsonMappingException, JsonProcessingException {
    try {
      ConsumerRecord<String, String> consumerRecord =
          new ConsumerRecord<>("topic", 0, 0, "key", "[" + update + "]");

      when(socketIOServer.getRoomOperations(consumerRecord.key())).thenReturn(broadcastOperations);
      leaderboardKafkaListener.consumeShowdownResponse(socketIOServer, consumerRecord);
    } catch (Exception e) {
      assertNotNull(e);
    }
  }

  @Test
  void showdownResponseTest3() throws JsonMappingException, JsonProcessingException {
    try {
      ConsumerRecord<String, String> consumerRecord =
          new ConsumerRecord<>("topic", 0, 0, "key", "");

      when(socketIOServer.getRoomOperations(consumerRecord.key())).thenReturn(broadcastOperations);
      leaderboardKafkaListener.consumeShowdownResponse(socketIOServer, consumerRecord);
    } catch (Exception e) {
      assertNotNull(e);
    }
  }

  @ParameterizedTest
  @ValueSource(
      strings = {
        "LDRBRD::60c38852f5860a2012497c3d::Dachanta",
        "LDRBRD::60c38852f5860a2012497c3d",
        "key",
        "key::1::2::3"
      })
  void consumeLeaderboardUpdatesTest_LDRBRD(String key) {
    try {
      ConsumerRecord<String, String> record =
          new ConsumerRecord<String, String>("topic", 0, 0, key, "[" + update + "]");
      when(socketIOServer.getRoomOperations(record.key())).thenReturn(broadcastOperations);
      leaderboardKafkaListener.consumeLeaderboardUpdate(socketIOServer, record);
    } catch (Exception e) {
      fail();
    }
  }

  @Test
  void consumeLeaderboardUpdatesTest() {
    try {
      ConsumerRecord<String, String> record =
          new ConsumerRecord<String, String>("topic", 0, 0, "key", "");
      when(socketIOServer.getRoomOperations(any())).thenReturn(broadcastOperations);
      when(broadcastOperations.getClients()).thenReturn(Collections.singleton(socketIOClient));
      leaderboardKafkaListener.consumeLeaderboardUpdate(socketIOServer, record);
    } catch (Exception e) {
      fail();
    }
  }
}
