package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.entity.TimelinePostSseEvent;
import java.time.LocalDateTime;
import java.util.List;
import java.util.UUID;
import java.util.concurrent.CopyOnWriteArrayList;
import java.util.concurrent.Executors;
import java.util.concurrent.ScheduledExecutorService;
import java.util.concurrent.TimeUnit;
import javax.annotation.PreDestroy;
import lombok.AllArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.web.servlet.mvc.method.annotation.ResponseBodyEmitter;
import org.springframework.web.servlet.mvc.method.annotation.SseEmitter;

@Slf4j
@Service
@AllArgsConstructor
public class TimelineSseService {
  protected static final List<SseEmitter> emitters = new CopyOnWriteArrayList<>();

  private static final ScheduledExecutorService DELAYED_EXECUTOR =
      Executors.newSingleThreadScheduledExecutor();
  private static final int INIT_MESSAGE_DELAY = 20;
  private static final long SSE_TIMEOUT_MS = TimeUnit.HOURS.toMillis(1);

  public SseEmitter createAndRegisterEmitter() {
    SseEmitter emitter = new SseEmitter(SSE_TIMEOUT_MS);
    emitter.onCompletion(() -> removeSilently(emitter));
    sendInitialEventAsync(emitter);
    emitters.add(emitter);
    return emitter;
  }

  private void sendInitialEventAsync(SseEmitter emitter) {
    DELAYED_EXECUTOR.schedule(
        () -> sendEvent(emitter, LocalDateTime.now()), INIT_MESSAGE_DELAY, TimeUnit.MILLISECONDS);
  }

  private void removeSilently(SseEmitter emitter) {
    try {
      emitters.remove(emitter);
    } catch (Exception e) {
      log.error("Failed to remove timeline emitter", e);
    }
  }

  public void populateEventForReceivers(TimelinePostSseEvent event) {
    emitters.forEach(emitter -> sendEvent(emitter, event));
  }

  private <T> void sendEvent(SseEmitter emitter, T event) {
    try {
      emitter.send(SseEmitter.event().data(event).id(UUID.randomUUID().toString()));
    } catch (Exception e) {
      log.warn("Failed to send timeline changed event to emitter", e);
      emitter.complete();
      removeSilently(emitter);
    }
  }

  @PreDestroy
  public void disconnect() {
    try {
      emitters.forEach(ResponseBodyEmitter::complete);
    } catch (Exception e) {
      log.warn("Failed to complete emitter", e);
    }
  }
}
