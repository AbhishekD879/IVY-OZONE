package com.entain.oxygen.betbuilder_middleware.service;

import com.google.gson.Gson;

public class BBUtil {

  public static final Gson gson = new Gson();

  private BBUtil() {}

  public static final String X_CORRELATION_ID = "X-Correlation-ID";
  public static final String CORRELATION_ID = "correlationId";
  public static final String TRANSACTION_PATH = "transactionPath";
  public static final String LCG_REQUEST = "LCGRequest";
  public static final String LCG_REQUEST_KEY = "lcg.request";
  public static final String BPG_REQUEST_KEY = "bpg.request";
  public static final String BPG_RESPONSE_KEY = "bpg.response";
  public static final String BPG_STATUS_KEY = "bpg.status";
  public static final String LCG_STATUS_KEY = "lcg.status";
  public static final String LCG_RESPONSE_KEY = "lcg.response";

  public static String toJson(Object obj) {
    String json = "";
    if (obj != null) {
      json = gson.toJson(obj);
    }
    return json;
  }
}
