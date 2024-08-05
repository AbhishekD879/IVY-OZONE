package com.egalacoral.spark.liveserver;

import com.egalacoral.spark.liveserver.utils.StringUtils;
import java.io.Serializable;
import lombok.extern.slf4j.Slf4j;

/** Created by vasylpirus on 5/2/16. */
@Slf4j
public class SubscriptionSubject implements Serializable {

  private static final long serialVersionUID = -7412637486447465101L;
  private static final int EVENT_ID_LENGTH = 10;

  private final ChannelType channel;
  private final String id;
  private String lastMessageID = "";

  public SubscriptionSubject(ChannelType channel, String id) {
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
