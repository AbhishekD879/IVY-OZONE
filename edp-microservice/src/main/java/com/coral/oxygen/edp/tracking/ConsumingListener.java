package com.coral.oxygen.edp.tracking;

import java.util.Map;

/** Request for consuming data */
public interface ConsumingListener<T, D> {

  void onResponse(Map<T, D> response);

  void onError(String message, Throwable t);
}
