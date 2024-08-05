package com.ladbrokescoral.cashout.socketio;

import com.corundumstudio.socketio.SocketIOServer;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import java.util.UUID;
import lombok.RequiredArgsConstructor;
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import reactor.core.publisher.Mono;

@RestController
@RequiredArgsConstructor
@ConditionalOnProperty(value = "qa.endpoint.enabled", matchIfMissing = true)
public class CashoutQAController {
  private final SocketIOServer socketIOServer;
  private final ObjectMapper objectMapper;

  @PostMapping(value = "/qa/socketio/send/{sid}", consumes = MediaType.APPLICATION_JSON_VALUE)
  public Mono<String> sendToSocketIoClient(
      @PathVariable("sid") String socketIoClientId,
      @RequestParam(required = true) String eventName,
      @RequestBody String payload)
      throws JsonProcessingException {
    socketIOServer
        .getClient(UUID.fromString(socketIoClientId))
        .sendEvent(eventName, objectMapper.readTree(payload));
    return Mono.just("done");
  }
}
