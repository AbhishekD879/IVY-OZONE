package com.egalacoral.spark.timeform.api;

/**
 * Callback for retrieving data from TimeForm
 * */
public interface DataCallback<T> {

  /**
   * This callback method will be called in case of success data receiving.
   * */
  void onResponse(T data);

  /**
   * This callback method will be called in case of internal exception or error response
   * */
  void onError(Throwable throwable);

}
