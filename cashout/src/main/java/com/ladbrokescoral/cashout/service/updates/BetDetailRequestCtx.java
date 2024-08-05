package com.ladbrokescoral.cashout.service.updates;

import com.coral.bpp.api.model.bet.api.request.GetBetDetailRequest;
import com.fasterxml.jackson.databind.annotation.JsonDeserialize;
import com.fasterxml.jackson.databind.annotation.JsonSerialize;
import com.fasterxml.jackson.datatype.jsr310.deser.DurationDeserializer;
import com.fasterxml.jackson.datatype.jsr310.ser.DurationSerializer;
import java.time.Duration;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@Builder
@AllArgsConstructor
@NoArgsConstructor
public class BetDetailRequestCtx {
  private GetBetDetailRequest request;
  private String userId;

  @JsonDeserialize(using = DurationDeserializer.class)
  @JsonSerialize(using = DurationSerializer.class)
  private Duration timeToTokenExpirationLeft;

  private long timestamp;
}
