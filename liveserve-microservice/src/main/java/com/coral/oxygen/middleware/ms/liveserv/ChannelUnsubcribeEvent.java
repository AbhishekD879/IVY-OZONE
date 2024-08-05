package com.coral.oxygen.middleware.ms.liveserv;

import java.util.Objects;
import org.springframework.context.ApplicationEvent;

/** Published when system should unsubcribe from <code>liveServChannel</code> */
public class ChannelUnsubcribeEvent extends ApplicationEvent {
  private final String liveServChannel;

  public ChannelUnsubcribeEvent(Object source, String liveServChannel) {
    super(source);
    this.liveServChannel = liveServChannel;
  }

  public String getLiveServChannel() {
    return liveServChannel;
  }

  @Override
  public boolean equals(Object o) {
    if (this == o) return true;
    if (o == null || getClass() != o.getClass()) return false;
    ChannelUnsubcribeEvent that = (ChannelUnsubcribeEvent) o;
    return Objects.equals(liveServChannel, that.liveServChannel);
  }

  @Override
  public int hashCode() {
    return Objects.hash(liveServChannel);
  }

  @Override
  public String toString() {
    final StringBuilder sb = new StringBuilder("ChannelUnsubcribeEvent{");
    sb.append("liveServChannel='").append(liveServChannel).append('\'');
    sb.append(", source=").append(source);
    sb.append('}');
    return sb.toString();
  }
}
