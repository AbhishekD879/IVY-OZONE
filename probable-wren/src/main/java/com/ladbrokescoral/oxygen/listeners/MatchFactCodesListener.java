package com.ladbrokescoral.oxygen.listeners;

import com.corundumstudio.socketio.AckRequest;
import com.corundumstudio.socketio.SocketIOClient;
import com.corundumstudio.socketio.listener.DataListener;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.ladbrokescoral.oxygen.dto.messages.IncidentMessage;
import com.ladbrokescoral.oxygen.service.RedisOperations;
import java.util.List;
import java.util.Optional;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Component;

@Slf4j
@Component
@RequiredArgsConstructor
public class MatchFactCodesListener implements DataListener<List<String>> {

  private final RedisOperations redisOperations;
  private final ObjectMapper objectMapper;
  private static final String FACT_MSG = "mFACTS";
  private static final int SIX = 6;

  /**
   * Invokes when data object received from client
   *
   * @param client - receiver
   * @param data - received object
   * @param ackSender - ack request
   * @throws Exception
   */
  @Override
  public void onData(SocketIOClient client, List<String> data, AckRequest ackSender)
      throws Exception {
    log.info("Starting MatchFactCodesListener onData {}", data);
    data.forEach(channel -> processLastIncidents(channel.substring(SIX), client));
  }

  private void processLastIncidents(String channel, SocketIOClient client) {
    log.info("processLastIncidents channel {} ", channel);
    redisOperations
        .getIncidentLastMessage(channel)
        .thenAccept(
            (Optional<IncidentMessage> optionalIncident) -> {
              if (optionalIncident.isPresent()) {
                IncidentMessage incidentMessage = optionalIncident.get();
                log.info("processLastIncidents incidentMessage {}", incidentMessage);
                try {
                  client.sendEvent(
                      FACT_MSG + incidentMessage.getChannel(),
                      objectMapper.readValue(
                          incidentMessage.getMessage(), new TypeReference<Object>() {}));
                } catch (JsonProcessingException e) {
                  log.error("Can not parse incidents message {}", e.getMessage());
                }
              }
            });
  }
}
