package com.ladbrokescoral.oxygen.timeline.api.channel;

import com.ladbrokescoral.oxygen.timeline.api.handlers.ReactiveWsMessageHandler;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.concurrent.ConcurrentHashMap;
import lombok.Getter;
import lombok.extern.slf4j.Slf4j;
import org.springframework.messaging.Message;
import reactor.core.publisher.Sinks;

@Slf4j
public class ChannelHandlersContext {

  private ChannelHandlersContext() {}

  @Getter
  public static final Map<String, ReactiveWsMessageHandler> wsHandlers = new ConcurrentHashMap<>();

  @Getter
  public static final Map<String, List<Sinks.Many<Message<?>>>> channels =
      new ConcurrentHashMap<>();

  @Getter
  public static final Map<String, Set<ReactiveWsMessageHandler>> messageHandlersPerPage =
      new ConcurrentHashMap<>();

  public static void createIfAbsentAndReturnChannel(String room) {
    channels.computeIfAbsent(
        room,
        (String s) -> {
          List<Sinks.Many<Message<?>>> sinkSet = new ArrayList<>();
          sinkSet.add(Sinks.many().multicast().onBackpressureBuffer(1, false));
          return sinkSet;
        });
  }
}
