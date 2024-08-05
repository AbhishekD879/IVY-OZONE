package com.coral.oxygen.middleware.pojos.model.output;

import com.fasterxml.jackson.annotation.JsonInclude;
import java.io.Serializable;
import java.time.Instant;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import lombok.Data;
import org.springframework.data.annotation.Id;
import org.springframework.data.redis.core.RedisHash;
import org.springframework.data.redis.core.index.Indexed;

@JsonInclude(JsonInclude.Include.NON_NULL)
@Data
@RedisHash(value = "${app.nextraces.hash}", timeToLive = -1L)
public class NextRaceFilterDto implements Serializable {
  @Id private String id;
  @Indexed private String categoryId;
  private Map<String, NextRacesClfDto> nextRaces = new HashMap<>();
  private List<String> virtualClassNames = new ArrayList<>();

  private String excludeTimeRange;

  private Instant excludeFrom;
  private Instant excludeTo;
}
