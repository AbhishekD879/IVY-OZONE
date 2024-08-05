package com.ladbrokescoral.oxygen.notification.services;

import com.google.gson.Gson;
import com.google.json.JsonSanitizer;
import com.ladbrokescoral.oxygen.notification.entities.bet.Betslip;
import com.ladbrokescoral.oxygen.notification.services.alert.WinAlertMessageHandler;
import lombok.extern.slf4j.Slf4j;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.messaging.handler.annotation.Payload;
import org.springframework.stereotype.Service;

/** Combines listeners for DF Kafka updates. Specifically, sportsbook and betslip topics. */
@Service
@Slf4j
public class KafkaListenerService {

  private NotificationsMessageHandler notificationsMessageHandler;
  private WinAlertMessageHandler winAlertMessageHandler;
  private Gson gson;

  public KafkaListenerService(
      NotificationsMessageHandler notificationsMessageHandler,
      WinAlertMessageHandler winAlertMessageHandler,
      Gson gson) {
    this.notificationsMessageHandler = notificationsMessageHandler;
    this.winAlertMessageHandler = winAlertMessageHandler;
    this.gson = gson;
  }

  @KafkaListener(topics = "${app.kafka.topic.sportsbook}")
  public void listenSportsBook(@Payload String message) {
    logger.info("Incoming SAF: {}", message);
    notificationsMessageHandler.handleSportsBookUpdate(message);
  }

  @KafkaListener(topics = "${app.kafka.topic.betslip}")
  public void listenWinAlert(@Payload String message) {
    String sanitizedMessage = JsonSanitizer.sanitize(message);
    Betslip betslip = gson.fromJson(sanitizedMessage, Betslip.class);
    winAlertMessageHandler.handleBetslip(betslip);
  }
}
