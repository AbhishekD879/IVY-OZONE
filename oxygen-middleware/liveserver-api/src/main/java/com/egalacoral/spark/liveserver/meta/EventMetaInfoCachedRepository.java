package com.egalacoral.spark.liveserver.meta;

import java.math.BigInteger;

public interface EventMetaInfoCachedRepository extends EventMetaInfoRepository {
  void putByEventId(BigInteger eventId, EventMetaInfo eventMetaInfo);

  void putBySelectionId(BigInteger selectionId, EventMetaInfo eventMetaInfo);

  void putByMarketId(BigInteger marketId, EventMetaInfo eventMetaInfo);

  default void putByEventId(BigInteger eventId, int categoryId) {
    putByEventId(eventId, EventMetaInfo.builder().eventId(eventId).categoryId(categoryId).build());
  }

  default void putBySelectionId(BigInteger selectionId, BigInteger eventId) {
    putBySelectionId(selectionId, EventMetaInfo.builder().eventId(eventId).build());
  }

  default void putByMarketId(BigInteger marketId, BigInteger eventId) {
    putByMarketId(marketId, EventMetaInfo.builder().eventId(eventId).build());
  }
}
