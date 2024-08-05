package com.entain.oxygen.bpp;

public interface BppProperties {

  int getRetryNumber();

  int getRetryTimeout();

  int getConnectTimeout();

  int getReadTimeout();

  int getWriteTimeout();

  int getPoolSize();

  int getThreads();

  boolean isKeepAlive();
}
