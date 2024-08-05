package com.ladbrokescoral.oxygen.dto.messages;

import java.io.Serializable;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.NoArgsConstructor;
import org.springframework.data.annotation.Id;
import org.springframework.data.redis.core.RedisHash;

@Data
@NoArgsConstructor
@EqualsAndHashCode
@RedisHash(value = "#{@distributedPrefix}", timeToLive = 50)
public class SimpleMessage implements Serializable {

  private static final long serialVersionUID = -6219345481563582289L;

  @Id private String channel;

  private String message;

  public SimpleMessage(String channel, String message) {
    this.channel = channel;
    this.message = message;
  }
}
