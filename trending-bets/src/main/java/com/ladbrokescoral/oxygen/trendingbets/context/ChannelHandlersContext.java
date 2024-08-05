package com.ladbrokescoral.oxygen.trendingbets.context;

import com.ladbrokescoral.oxygen.trendingbets.handler.ReactiveWsMessageHandler;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;
import lombok.Getter;
import lombok.extern.slf4j.Slf4j;
import org.springframework.messaging.Message;
import reactor.core.publisher.Sinks;

@Slf4j
public class ChannelHandlersContext {

  private ChannelHandlersContext() {}

  @Getter
  private static final Map<String, ReactiveWsMessageHandler> wsHandlers = new ConcurrentHashMap<>();

  @Getter
  private static final Map<String, Sinks.Many<Message<String>>> channels =
      new ConcurrentHashMap<>();

  public static Sinks.Many<Message<String>> createIfAbsentAndReturnChannel(String channelId) {
    return ChannelHandlersContext.getChannels()
        .computeIfAbsent(channelId, (String s) -> Sinks.many().multicast().directBestEffort());
  }
}
