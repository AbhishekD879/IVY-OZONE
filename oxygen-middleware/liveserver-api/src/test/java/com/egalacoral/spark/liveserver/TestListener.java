package com.egalacoral.spark.liveserver;

import java.util.ArrayList;
import java.util.List;

public class TestListener implements LiveServerListener {

  public List<Message> messages = new ArrayList<>();

  @Override
  public void onMessage(Message message) {
    messages.add(message);
  }

  @Override
  public void onError(Throwable e) {}
}
