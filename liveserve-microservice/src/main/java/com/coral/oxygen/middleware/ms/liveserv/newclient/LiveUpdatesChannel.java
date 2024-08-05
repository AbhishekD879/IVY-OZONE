package com.coral.oxygen.middleware.ms.liveserv.newclient;

import com.coral.oxygen.middleware.ms.liveserv.model.ChannelType;
import com.coral.oxygen.middleware.ms.liveserv.utils.StringUtils;
import java.io.Serializable;
import java.util.Objects;
import lombok.extern.slf4j.Slf4j;

@Slf4j
public class LiveUpdatesChannel implements Serializable {
  private static final long serialVersionUID = -7412637486447465101L;
  private static final int EVENT_ID_LENGTH = 10;

  private final ChannelType channel;
  private final String id;
  private String lastMessageID = "";

  public LiveUpdatesChannel(ChannelType channel, String id) {
    this.channel = channel;
    this.id = id;
  }

  public void addLastMessageID(String lastMessageId) {
    log.debug("add last message key {}", lastMessageId);
    this.lastMessageID = lastMessageId;
  }

  public String getKeyValue() {
    StringBuilder keyBuilder = new StringBuilder();
    keyBuilder.append(channel.getName());
    keyBuilder.append(StringUtils.addLeadingZeros(id, EVENT_ID_LENGTH));
    return keyBuilder.toString();
  }

  public String getLastMessageID() {
    return lastMessageID;
  }

  public String getUpdatedKeyValue() {
    StringBuilder keyBuilder = new StringBuilder();
    keyBuilder.append("S0001");
    keyBuilder.append(channel.getName());
    keyBuilder.append(StringUtils.addLeadingZeros(id, EVENT_ID_LENGTH));
    keyBuilder.append(lastMessageID);
    return keyBuilder.toString();
  }

  public String messageHashKey() {
    StringBuilder keyBuilder = new StringBuilder();
    keyBuilder.append("M");
    keyBuilder.append(channel.getName());
    keyBuilder.append(StringUtils.addLeadingZeros(id, EVENT_ID_LENGTH));
    return keyBuilder.toString();
  }

  @Override
  public boolean equals(Object o) {
    if (this == o) return true;
    if (o == null || getClass() != o.getClass()) return false;
    LiveUpdatesChannel that = (LiveUpdatesChannel) o;
    return channel == that.channel && Objects.equals(id, that.id);
  }

  @Override
  public int hashCode() {
    return Objects.hash(channel, id);
  }

  @Override
  public String toString() {
    return "SubscriptionSubject{"
        + "channel="
        + channel
        + ", id='"
        + id
        + '\''
        + ", lastMessageID='"
        + lastMessageID
        + '\''
        + '}';
  }
}
