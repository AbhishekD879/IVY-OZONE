package com.egalacoral.spark.liveserver.meta;

import java.math.BigInteger;
import lombok.Builder;
import lombok.EqualsAndHashCode;
import lombok.Getter;

@Builder
@Getter
@EqualsAndHashCode
public class EventMetaInfo {
  private final BigInteger eventId;
  private final int categoryId;
}
