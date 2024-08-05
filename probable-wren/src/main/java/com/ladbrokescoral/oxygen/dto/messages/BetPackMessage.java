package com.ladbrokescoral.oxygen.dto.messages;

import com.ladbrokescoral.oxygen.model.FreebetOffer;
import java.io.Serializable;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.NoArgsConstructor;
import org.springframework.data.annotation.Id;
import org.springframework.data.redis.core.RedisHash;

@Data
@NoArgsConstructor
@EqualsAndHashCode
@RedisHash(value = "#{@distributedPrefix}_bpmp", timeToLive = 604800)
public class BetPackMessage implements Serializable {

  private static final long serialVersionUID = -6219345481563582289L;

  @Id private String betPackId;

  private FreebetOffer message;

  public BetPackMessage(String betPackId, FreebetOffer message) {
    this.betPackId = betPackId;
    this.message = message;
  }
}
