package com.egalacoral.spark.liveserver;

public interface LiveServerListener {

  void onMessage(Message message);

  void onError(Throwable e);
}
