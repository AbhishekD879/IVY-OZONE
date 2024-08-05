package com.ladbrokescoral.oxygen.notification.entities.dto;

import java.io.Serializable;
import java.util.Date;
import lombok.*;
import org.springframework.data.redis.core.RedisHash;

@Data
@ToString
@Builder
@EqualsAndHashCode(of = {"betId", "token", "platform"})
@RedisHash("win_alert_subscriptions")
public class WinAlertDTO implements Serializable {
  private String betId;
  private String token;
  private String platform;
  private String userName;
  private final Date dateCreated = new Date();
  private final Integer appVersionInt;

  @Override
  public String toString() {
    return "WinAlertDTO{"
        + "betId='"
        + betId
        + '\''
        + ", token='"
        + token
        + '\''
        + ", platform='"
        + platform
        + '\''
        + ", userName='"
        + userName
        + '\''
        + ", dateCreated="
        + dateCreated
        + ", appVersionInt="
        + appVersionInt
        + '}';
  }
}
