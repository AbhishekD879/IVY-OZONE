package com.coral.oxygen.middleware.ms.liveserv.newclient.liveserve;

import java.security.KeyManagementException;
import java.security.NoSuchAlgorithmException;
import okhttp3.logging.HttpLoggingInterceptor;

public interface CallFactory {

  public Call createCall(
      long connectTimeout, long readTimeOut, HttpLoggingInterceptor.Level loggingLevel)
      throws NoSuchAlgorithmException, KeyManagementException;
}
