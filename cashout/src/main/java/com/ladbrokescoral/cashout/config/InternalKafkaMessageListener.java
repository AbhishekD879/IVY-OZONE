package com.ladbrokescoral.cashout.config;

import com.corundumstudio.socketio.BroadcastOperations;
import com.corundumstudio.socketio.SocketIOServer;
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Configuration;
import org.springframework.kafka.annotation.KafkaListener;

@Configuration
public class InternalKafkaMessageListener {

  @Autowired private SocketIOServer socketIOServer;

  private static final Logger ASYNC_LOGGER = LogManager.getLogger("ASYNC_JSON_FILE_APPENDER");

  @KafkaListener(
      groupId = "${payout-updates.consumer-group}-${random.uuid}",
      topics = "payout-updates",
      concurrency = "${payout-updates.consumer.concurrency:1}",
      containerFactory = "kafkaPayoutUpdateContainerFactory")
  public void onPayoutUpdate(ConsumerRecord<String, Object> payoutUpdateRecord) {
    String token = payoutUpdateRecord.key();
    Object payoutResponse = payoutUpdateRecord.value();
    ASYNC_LOGGER.info(
        "PayoutUpdate consumed for Token:{} PayoutResponse:{}", token, payoutResponse);
    BroadcastOperations roomOperations = socketIOServer.getRoomOperations(token);
    roomOperations.sendEvent("payoutUpdate", payoutResponse);
  }

  @KafkaListener(
      groupId = "${event-updates.consumer-group}-${random.uuid}",
      topics = "event-updates",
      concurrency = "${event-updates.consumer.concurrency:1}",
      containerFactory = "kafkaEventUpdateContainerFactory")
  public void onEventUpdate(ConsumerRecord<String, Object> eventUpdateRecord) {
    String token = eventUpdateRecord.key();
    Object eventResponse = eventUpdateRecord.value();
    ASYNC_LOGGER.info("EventUpdate consumed for Token:{} EventResponse:{}", token, eventResponse);
    BroadcastOperations roomOperations = socketIOServer.getRoomOperations(token);
    roomOperations.sendEvent("eventUpdate", eventResponse);
  }

  @KafkaListener(
      groupId = "${twoup_updates.consumer-group}-${random.uuid}",
      topics = "twoup_updates",
      concurrency = "${twoup_updates.consumer.concurrency:1}",
      containerFactory = "kafkaTwoUpUpdateContainerFactory")
  public void onTwoUpUpdate(ConsumerRecord<String, Object> twoUpUpdateRecord) {
    String token = twoUpUpdateRecord.key();
    Object twoUpUpdateResponse = twoUpUpdateRecord.value();
    ASYNC_LOGGER.debug(
        "TwoUpUpdate consumed for token : {}, twoUp response : {}", token, twoUpUpdateResponse);
    BroadcastOperations roomOperations = socketIOServer.getRoomOperations(token);
    roomOperations.sendEvent("twoUpUpdate", twoUpUpdateResponse);
  }
}
