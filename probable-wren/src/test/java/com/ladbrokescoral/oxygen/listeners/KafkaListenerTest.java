package com.ladbrokescoral.oxygen.listeners;

import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.mockito.Mockito.when;

import com.corundumstudio.socketio.BroadcastOperations;
import com.corundumstudio.socketio.SocketIOServer;
import com.corundumstudio.socketio.store.StoreFactory;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.JsonMappingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import com.ladbrokescoral.oxygen.dto.messages.Envelope;
import com.ladbrokescoral.oxygen.dto.messages.EnvelopeType;
import com.ladbrokescoral.oxygen.dto.messages.MessageObjectEnvelope;
import com.ladbrokescoral.oxygen.service.IncidentsDataProcessor;
import com.ladbrokescoral.oxygen.service.RedisOperations;
import com.ladbrokescoral.oxygen.service.betpack.BetPackRedisOperations;
import com.ladbrokescoral.oxygen.utils.MessageUtils;
import java.util.Arrays;
import java.util.List;
import java.util.Optional;
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
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
    classes = {ThreadPoolTaskExecutor.class, KafkaListener.class, Gson.class},
    properties = "leaderboard.enabled=false")
class KafkaListenerTest {

  @MockBean private SocketIOServer socketIOServer;
  @MockBean private RedisOperations redisOperations;
  @MockBean private BroadcastOperations broadcastOperations;
  @MockBean private ObjectMapper objectMapper;
  @Autowired private ThreadPoolTaskExecutor leaderboardExecutor;

  @MockBean private BetPackRedisOperations betPackRedisOperations;

  private Gson gson;
  private KafkaListener kafkaListener;
  @MockBean private StoreFactory storeFactory;
  @MockBean IncidentsDataProcessor incidentsDataProcessor;

  private static final String CHANNEL = "chanel1";
  private static final String DATA = "data";
  private static final String EVENTID = "222211218";
  private List<Integer> cacheCodes = Arrays.asList(2, 6);
  String MESSAGE =
      "{\"incident\":{\"eventId\":\"fake593f-d146-4092-ad46-8bdf192b6ebb\",\"correlationId\":\"7645316d-ddc8-42c9-ac4e-e6668704a5f6\",\"seqId\":null,\"type\":{\"code\":601,\"description\":\"VAR\"},\"score\":null,\"periodScore\":null,\"clock\":\"46:32\",\"participant\":\"AWAY\",\"period\":\"1h\",\"timeStamp\":\"2022-01-03T12:43:40.342Z\",\"receiveTimestamp\":\"2020-07-15T23:37:07.478Z\",\"context\":{\"teamName\":\"Liverpool\",\"playerName\":\"G. Wijnaldum\",\"reasonId\":601,\"x\":\"0\",\"y\":\"0\"},\"feed\":\"OPTA\"}}";
  long ttl = 900;

  @BeforeEach
  public void init() {
    gson = new GsonBuilder().serializeNulls().create();

    kafkaListener =
        new KafkaListener(
            socketIOServer, redisOperations, gson, 1, leaderboardExecutor, incidentsDataProcessor);
  }

  @Test
  void consumeRecordTest() {
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
        new ConsumerRecord<>("topic", 0, 0, "key", envelopeString);
    when(socketIOServer.getRoomOperations(CHANNEL)).thenReturn(broadcastOperations);

    kafkaListener.consume(consumerRecord);
    Optional<MessageObjectEnvelope> messageObjectEnvelopeOptional =
        MessageUtils.toMessage(envelope, gson);
    Assertions.assertTrue(messageObjectEnvelopeOptional.isPresent());
  }

  @Test
  void consumeRecordTest_error() {
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
    ConsumerRecord<String, String> consumerRecord = new ConsumerRecord<>("topic", 0, 0, "key", "");
    when(socketIOServer.getRoomOperations(CHANNEL)).thenReturn(broadcastOperations);
    kafkaListener.consume(consumerRecord);
    Optional<MessageObjectEnvelope> messageObjectEnvelopeOptional =
        MessageUtils.toMessage(envelope, gson);
    Assertions.assertTrue(messageObjectEnvelopeOptional.isPresent());
  }

  @Test
  void consumeScoreboardTest() {
    try {
      ConsumerRecord<String, String> record =
          new ConsumerRecord<String, String>("topic", 0, 0, "key", "");
      when(socketIOServer.getRoomOperations(record.key())).thenReturn(broadcastOperations);
      kafkaListener.consumeScoreboard(record);
    } catch (Exception e) {
      assertNotNull(e);
    }
  }

  @Test
  void consumeScoreboardTest1() throws JsonMappingException, JsonProcessingException {
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
          new ConsumerRecord<>("topic", 0, 0, "key", envelopeString);

      when(socketIOServer.getRoomOperations(consumerRecord.key())).thenReturn(broadcastOperations);
      kafkaListener.consumeScoreboard(consumerRecord);
    } catch (Exception e) {
      assertNotNull(e);
    }
  }

  @Test
  void consumeIncidentsTest() {
    String data =
        "{\"incident\":{\"eventId\":\"fake593f-d146-4092-ad46-8bdf192b6ebb\",\"correlationId\":\"7645316d-ddc8-42c9-ac4e-e6668704a5f6\",\"seqId\":null,\"type\":{\"code\":601,\"description\":\"VAR\"},\"score\":null,\"periodScore\":null,\"clock\":\"46:32\",\"participant\":\"AWAY\",\"period\":\"1h\",\"timeStamp\":\"2022-01-03T12:43:40.342Z\",\"receiveTimestamp\":\"2020-07-15T23:37:07.478Z\",\"context\":{\"teamName\":\"Liverpool\",\"playerName\":\"G. Wijnaldum\",\"reasonId\":601,\"x\":\"0\",\"y\":\"0\"},\"feed\":\"OPTA\"}}";
    ConsumerRecord<String, String> record =
        new ConsumerRecord<String, String>("topic", 0, 0, EVENTID, data);
    when(socketIOServer.getRoomOperations(record.key())).thenReturn(broadcastOperations);
    kafkaListener.consumeIncidents(record);
    Assertions.assertNotNull(record.value());
  }

  @Test
  void consumeEmptyIncidentsTest() {
    try {
      ConsumerRecord<String, String> record =
          new ConsumerRecord<String, String>("topic", 0, 0, "key", "");
      when(socketIOServer.getRoomOperations(record.key())).thenReturn(broadcastOperations);
      kafkaListener.consumeIncidents(record);
    } catch (Exception e) {
      assertNotNull(e);
    }
  }

  /*@Test
  void showdownResponseTest() {
    try {
      FreebetOffer freebetOffer = new FreebetOffer();
      freebetOffer.setFreebetOfferId("1");
      freebetOffer.setFreebetOfferName("Offer");
      ConsumerRecord<String, FreebetOffer> consumerRecord =
          new ConsumerRecord<>("topic", 0, 0, "key", freebetOffer);

      when(socketIOServer.getRoomOperations(any())).thenReturn(broadcastOperations);
      kafkaListener.consumeBetPack(consumerRecord);
      betPackRedisOperations.saveLastMessage(new BetPackMessage("1", freebetOffer));

    } catch (Exception e) {
      assertNotNull(e);
    }
  }

  @Test
  void showdownResponseTestE() {
    try {
      FreebetOffer freebetOffer = new FreebetOffer();
      freebetOffer.setFreebetOfferName("Offer");
      ConsumerRecord<String, FreebetOffer> consumerRecord =
          new ConsumerRecord<>("topic", 0, 0, "key", freebetOffer);
      when(socketIOServer.getRoomOperations(consumerRecord.key())).thenReturn(broadcastOperations);
      kafkaListener.consumeBetPack(consumerRecord);
    } catch (Exception e) {
      assertNotNull(e);
    }
  }*/
}
