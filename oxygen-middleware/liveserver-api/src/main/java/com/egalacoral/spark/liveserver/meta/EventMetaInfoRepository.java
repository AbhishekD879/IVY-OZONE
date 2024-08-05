package com.egalacoral.spark.liveserver.meta;

import java.math.BigInteger;
import java.util.Optional;

public interface EventMetaInfoRepository {
  Optional<EventMetaInfo> getBySelectionId(BigInteger selectionId);

  Optional<EventMetaInfo> getByMarketId(BigInteger marketId);

  Optional<EventMetaInfo> getByEventId(BigInteger eventId);
}
