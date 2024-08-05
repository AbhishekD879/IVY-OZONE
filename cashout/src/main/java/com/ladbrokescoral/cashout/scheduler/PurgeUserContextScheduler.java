package com.ladbrokescoral.cashout.scheduler;

import com.corundumstudio.socketio.SocketIOClient;
import com.corundumstudio.socketio.SocketIOServer;
import com.ladbrokescoral.cashout.service.BetUpdateService;
import java.util.List;
import java.util.Optional;
import java.util.UUID;
import java.util.stream.Collectors;
import lombok.extern.slf4j.Slf4j;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;

@Component
@Slf4j
public class PurgeUserContextScheduler {
  private final BetUpdateService betUpdateService;
  private final SocketIOServer customSocketIOServer;

  public PurgeUserContextScheduler(
      BetUpdateService betUpdateService, SocketIOServer customSocketIOServer) {
    this.betUpdateService = betUpdateService;
    this.customSocketIOServer = customSocketIOServer;
  }

  @Scheduled(cron = "${cashout.userContext.cron.expression}")
  public void processUserContext() {

    try {
      List<UUID> uuids =
          betUpdateService.getUserContexts().keySet().stream().collect(Collectors.toList());
      int size = uuids.size();

      uuids.stream()
          .parallel()
          .forEach(
              (UUID uuid) -> {
                Optional<SocketIOClient> client =
                    Optional.ofNullable(customSocketIOServer.getClient(uuid));

                if ((!client.isPresent()) || (!client.get().isChannelOpen()))
                  betUpdateService.unsubscribeInInternalPubSub(uuid);
              });

      log.debug(
          "Cleanup task executed : Before {}, After {}",
          size,
          betUpdateService.getUserContexts().size());

    } catch (Exception e) {
      log.error("error while processing processUserContext ", e);
    }
  }
}
