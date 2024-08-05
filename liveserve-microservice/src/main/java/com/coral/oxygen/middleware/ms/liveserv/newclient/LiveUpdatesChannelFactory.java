package com.coral.oxygen.middleware.ms.liveserv.newclient;

import com.coral.oxygen.middleware.ms.liveserv.model.ChannelType;
import com.coral.oxygen.middleware.ms.liveserv.utils.StringUtils;
import java.util.Objects;
import lombok.extern.slf4j.Slf4j;

/**
 * @author volodymyr.masliy
 */
@Slf4j
public class LiveUpdatesChannelFactory {

  private LiveUpdatesChannelFactory() {}

  public static LiveUpdatesChannel onEventSubscription(String eventId) {
    return new LiveUpdatesChannel(ChannelType.sEVENT, eventId);
  }

  public static LiveUpdatesChannel onMarketSubscription(String marketId) {
    return new LiveUpdatesChannel(ChannelType.sEVMKT, marketId);
  }

  public static LiveUpdatesChannel onSelectionSubscription(String selectionId) {
    return new LiveUpdatesChannel(ChannelType.sSELCN, selectionId);
  }

  public static LiveUpdatesChannel onScoreSubscription(String eventId) {
    return new LiveUpdatesChannel(ChannelType.sSCBRD, eventId);
  }

  public static LiveUpdatesChannel onAggregatedSubscription(String eventId) {
    return new LiveUpdatesChannel(ChannelType.SEVENT, eventId);
  }

  public static LiveUpdatesChannel onClockSubscription(String eventId) {
    return new LiveUpdatesChannel(ChannelType.sCLOCK, eventId);
  }

  /**
   * Constructs instance of #{@link LiveUpdatesChannel} from standard string channel representation
   * For example: sEVENT0102030405
   */
  public static LiveUpdatesChannel fromString(String channel) {
    Objects.requireNonNull(channel, "channel");
    String channelId = channel.substring(6);
    if (channel.length() < 16) {
      String errorMsg = "Channel " + channel + " length is less then 16 symbols";
      log.warn(errorMsg);
      throw new IllegalArgumentException(errorMsg);
    }

    if (channel.length() > 16) {
      log.warn("Channel {} length exceeds 16 symbols, trying to trim redundant '0'", channel);
      channelId = StringUtils.tryTrimChannelPrefix(channelId);
    }
    ChannelType channelType = ChannelType.valueOf(channel.substring(0, 6));
    return new LiveUpdatesChannel(channelType, channelId);
  }
}
