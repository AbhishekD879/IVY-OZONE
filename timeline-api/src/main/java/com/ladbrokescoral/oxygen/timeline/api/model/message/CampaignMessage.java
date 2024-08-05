package com.ladbrokescoral.oxygen.timeline.api.model.message;

import java.io.Serializable;
import java.time.Instant;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.ToString;
import lombok.experimental.Accessors;
import org.springframework.data.annotation.Id;
import org.springframework.data.redis.core.RedisHash;
import org.springframework.data.redis.core.index.Indexed;

@Data
@ToString(callSuper = true)
@EqualsAndHashCode(callSuper = true)
@Accessors(chain = true)
@RedisHash("campaignMessages")
public class CampaignMessage extends Message implements Serializable {
  @Id private String id;
  @Indexed private Instant createdDate;
  @Indexed private String brand;
  @Indexed private Instant displayFrom;
  @Indexed private Instant displayTo;
  private int pageSize;
}
