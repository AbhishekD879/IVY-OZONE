package com.ladbrokescoral.oxygen.trendingbets.liveserv.updates;

import java.util.List;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Component;

@Component
@RequiredArgsConstructor
public class LiveserveMessageApplierFactory {

  private final List<ChannelMessageApplier> channelMessageApplierTypes;

  public ChannelMessageApplier get(String channel) {
    return channelMessageApplierTypes.stream()
        .filter(channelPrefix -> channel.startsWith(channelPrefix.type()))
        .findAny()
        .orElseThrow(
            () ->
                new IllegalArgumentException("No defined message applier for channel: " + channel));
  }
}
