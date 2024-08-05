package com.entain.oxygen.service;

import com.entain.oxygen.exceptions.RTMSException;
import com.entain.oxygen.kafka.GlobalKafkaPublisher;
import com.entain.oxygen.model.*;
import com.entain.oxygen.util.JsonUtil;
import com.google.gson.Gson;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Optional;
import java.util.UUID;
import lombok.extern.slf4j.Slf4j;
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.springframework.stereotype.Service;

@Service
@Slf4j
public class RtmsKafkaPublisherService {

  private GlobalKafkaPublisher globalKafkaPublisher;

  public RtmsKafkaPublisherService(GlobalKafkaPublisher globalKafkaPublisher) {
    this.globalKafkaPublisher = globalKafkaPublisher;
  }

  public void processMessage(ConsumerRecord<String, String> dfUpdate) {
    log.info("Fanzone Preference change update from DF  :: {}", dfUpdate.value());
    FanzonePlayerPreferences kafkaUpdate =
        JsonUtil.fromJson(dfUpdate.value(), FanzonePlayerPreferences.class);
    UUID uuid = UUID.randomUUID();

    RtmsDto message = toRtmsDto(kafkaUpdate, uuid);

    log.info("UPMS team change update :: {}", new Gson().toJson(message));

    globalKafkaPublisher.publishMessage(
        dfUpdate.key(), new Gson().toJson(message), Optional.empty());
  }

  public RtmsDto toRtmsDto(FanzonePlayerPreferences kafkaUpdate, UUID uuid) {

    SimpleDateFormat df = new SimpleDateFormat("yyyy-MM-dd'T'hh:mm:ssZ");
    Date date = null;
    try {
      date = df.parse(kafkaUpdate.getTeamLastUpdatedDate());
    } catch (ParseException e) {
      throw new RTMSException(e.getMessage());
    }
    RtmsDto rtmsDto = new RtmsDto();
    rtmsDto.setEventId(uuid.toString());
    rtmsDto.setEventType("FZ_EVENT");
    rtmsDto.setUserId(kafkaUpdate.getAccountName());
    rtmsDto.setFrontend("ld");
    rtmsDto.setBrand(kafkaUpdate.getBrand());
    rtmsDto.setProduct(kafkaUpdate.getProduct());
    rtmsDto.setChannel("*");
    rtmsDto.setEventCreationTime(date.getTime());

    Payload payload = new Payload();
    payload.setUserName(kafkaUpdate.getAccountName());
    Preferences preferences = new Preferences();
    preferences.setTEAM_ID(kafkaUpdate.getPreferences().getTEAM_ID());
    preferences.setTEAM_NAME(kafkaUpdate.getPreferences().getTEAM_NAME());
    payload.setPreferencesObject(preferences);
    rtmsDto.setPayload(payload);

    CustomHeaders customHeaders = new CustomHeaders();
    customHeaders.setIS_PRIVILEGED_MSG(true);
    customHeaders.setSOURCE("FANZONE");
    customHeaders.setNOTIFICATION_TYPE("FZ_PLAYER_PREFS");
    rtmsDto.setCustomHeaders(customHeaders);
    log.info("UPMS team change update :: {}", new Gson().toJson(rtmsDto));
    return rtmsDto;
  }
}
