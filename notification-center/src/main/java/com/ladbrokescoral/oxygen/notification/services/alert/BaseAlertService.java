package com.ladbrokescoral.oxygen.notification.services.alert;

import com.ladbrokescoral.oxygen.notification.entities.BaseSubscription;
import lombok.extern.slf4j.Slf4j;

/**
 * The abstraction here could be simplified, it is unnecessary. Saves given subscription for
 * notifications.
 */
@Slf4j
public abstract class BaseAlertService implements AlertService {

  private long defaultWinAlertTimeoutHours;

  public BaseAlertService(long timeout) {
    this.defaultWinAlertTimeoutHours = timeout;
  }

  @Override
  public BaseSubscription save(BaseSubscription request) {

    long timeout = request.getHoursToExpire();
    if (timeout == 0) {
      timeout = defaultWinAlertTimeoutHours;
    }

    return saveInternal(request, timeout);
  }

  protected abstract BaseSubscription saveInternal(BaseSubscription request, long timeout);
}
