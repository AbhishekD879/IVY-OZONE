package com.coral.oxygen.middleware.ms.liveserv.model;

public interface SubscriptionStats {
  String getChannel();

  long getEventId();

  String getWaterMark();

  void setWaterMark(String waterMark);

  long getUpdatesCount();

  void setUpdatesCount(long updatesCount);

  long getLasSuccessUpdate();

  void setLasSuccessUpdate(long lasSuccessUpdate);

  long getLastError();

  void setLastError(long lastError);

  int getLastErrorsCount();

  void setLastErrorsCount(int lastErrorsCount);
}
