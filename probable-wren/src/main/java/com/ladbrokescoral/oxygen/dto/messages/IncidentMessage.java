package com.ladbrokescoral.oxygen.dto.messages;

import java.io.Serializable;
import java.util.concurrent.TimeUnit;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.NoArgsConstructor;
import org.springframework.data.annotation.Id;
import org.springframework.data.redis.core.RedisHash;
import org.springframework.data.redis.core.TimeToLive;

@Data
@NoArgsConstructor
@EqualsAndHashCode
@RedisHash("incidents")
public class IncidentMessage implements Serializable {

  private static final long serialVersionUID = -6218332181567585589L;

  @Id private String channel;

  private String message;

  @TimeToLive(unit = TimeUnit.SECONDS)
  private long ttl;

  public IncidentMessage(String channel, String message, long ttl) {
    this.channel = channel;
    this.message = message;
    this.ttl = ttl;
  }
}
