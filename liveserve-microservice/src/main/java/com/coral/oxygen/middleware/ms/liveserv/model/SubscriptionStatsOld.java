package com.coral.oxygen.middleware.ms.liveserv.model;

/** Created by azayats on 08.05.17. */
public class SubscriptionStatsOld implements SubscriptionStats {

  private final String channel;

  private final long eventId;

  private String waterMark;

  private long updatesCount;

  private long lasSuccessUpdate;

  private long lastError;

  private int lastErrorsCount;

  public SubscriptionStatsOld(String channel, long eventId) {
    this.channel = channel;
    this.eventId = eventId;
  }

  @Override
  public String getChannel() {
    return channel;
  }

  @Override
  public long getEventId() {
    return eventId;
  }

  @Override
  public String getWaterMark() {
    return waterMark;
  }

  @Override
  public void setWaterMark(String waterMark) {
    this.waterMark = waterMark;
  }

  @Override
  public long getUpdatesCount() {
    return updatesCount;
  }

  @Override
  public void setUpdatesCount(long updatesCount) {
    this.updatesCount = updatesCount;
  }

  @Override
  public long getLasSuccessUpdate() {
    return lasSuccessUpdate;
  }

  @Override
  public void setLasSuccessUpdate(long lasSuccessUpdate) {
    this.lasSuccessUpdate = lasSuccessUpdate;
  }

  @Override
  public long getLastError() {
    return lastError;
  }

  @Override
  public void setLastError(long lastError) {
    this.lastError = lastError;
  }

  @Override
  public int getLastErrorsCount() {
    return lastErrorsCount;
  }

  @Override
  public void setLastErrorsCount(int lastErrorsCount) {
    this.lastErrorsCount = lastErrorsCount;
  }

  @Override
  public String toString() {
    final StringBuilder sb = new StringBuilder("SubscriptionStats{");
    sb.append("channel='").append(channel).append('\'');
    sb.append(", eventId=").append(eventId);
    sb.append(", waterMark='").append(waterMark).append('\'');
    sb.append(", updatesCount=").append(updatesCount);
    sb.append(", lasSuccessUpdate=").append(lasSuccessUpdate);
    sb.append(", lastError=").append(lastError);
    sb.append(", lastErrorsCount=").append(lastErrorsCount);
    sb.append('}');
    return sb.toString();
  }
}
