package com.ladbrokescoral.oxygen.listeners;

import com.corundumstudio.socketio.AckRequest;
import com.corundumstudio.socketio.SocketIOClient;
import com.corundumstudio.socketio.listener.DataListener;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.ladbrokescoral.oxygen.service.ScoreboardEventStorageService;
import java.util.Map;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Component;

@Slf4j
@Component
@RequiredArgsConstructor
public class ScoreboardListener implements DataListener<String> {

  private final ScoreboardEventStorageService scoreboardService;
  private final ObjectMapper mapper;

  @Override
  public void onData(SocketIOClient client, String obEventId, AckRequest ackSender) {
    log.info("Starting to work with eventId: {}", obEventId);
    if (client.isChannelOpen()) {
      client.joinRoom(obEventId);
      scoreboardService
          .getInitialData(obEventId)
          .ifPresent(
              eventStatsModelDto -> {
                try {
                  Map<String, Object> stringObjectMap =
                      mapper.readValue(
                          eventStatsModelDto, new TypeReference<Map<String, Object>>() {});
                  client.sendEvent(obEventId, stringObjectMap.values().iterator().next());
                } catch (JsonProcessingException e) {
                  log.error("Cannont parse scoreboard update {}", e.getMessage());
                }
              });
    } else {
      log.warn("Client got disconected with IP:{}", client.getRemoteAddress().toString());
      client.disconnect();
    }
  }
}
