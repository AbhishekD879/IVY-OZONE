package com.coral.oxygen.middleware.common.imdg;

/**
 * @author volodymyr.masliy
 */
public interface DistributedTopicStats {
  Long getCreationTime();

  Long getPublishOperationCount();

  Long getReceiveOperationCount();
}
