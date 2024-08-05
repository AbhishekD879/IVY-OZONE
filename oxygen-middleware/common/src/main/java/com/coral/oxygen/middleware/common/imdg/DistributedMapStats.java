package com.coral.oxygen.middleware.common.imdg;

/**
 * @author volodymyr.masliy
 */
public interface DistributedMapStats {
  long getBackupCount();

  Long getBackupEntryCount();

  Long getBackupEntryMemoryCost();

  Long getCreationTime();

  Long getLastAccessTime();

  Long getLastUpdateTime();

  Long getHeapCost();

  Long getHits();

  Long getLockedEntryCount();

  Long getDirtyEntryCount();

  Long getEventOperationCount();

  Long getOwnedEntryMemoryCost();
}
