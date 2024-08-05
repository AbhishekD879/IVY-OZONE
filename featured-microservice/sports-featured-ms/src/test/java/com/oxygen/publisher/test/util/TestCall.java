package com.oxygen.publisher.test.util;

import java.io.IOException;
import java.util.Optional;
import okhttp3.Request;
import okio.Timeout;
import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

/**
 * @param <T> call response type
 * @author tvuyiv
 */
public class TestCall<T> implements Call<T> {

  private final String testUrl;
  private T response;
  private Throwable throwable;

  public TestCall(String testUrl, T response) {
    this.response = response;
    this.testUrl = testUrl;
  }

  public TestCall(String testUrl, Throwable throwable) {
    this.throwable = throwable;
    this.testUrl = testUrl;
  }

  @Override
  public Response<T> execute() throws IOException {
    return Response.success(response);
  }

  @Override
  public void enqueue(Callback<T> callback) {
    if (response != null) {
      callback.onResponse(this, Response.success(response));
    } else {
      callback.onFailure(this, Optional.of(throwable).orElseGet(IllegalStateException::new));
    }
  }

  @Override
  public boolean isExecuted() {
    return false;
  }

  @Override
  public void cancel() {
    // do nothing.
  }

  @Override
  public boolean isCanceled() {
    return false;
  }

  public TestCall<T> clone() {
    try {
      super.clone();
      return new TestCall(this.testUrl, this.response);
    } catch (CloneNotSupportedException e) {
      e.printStackTrace();
    }
    return null;
  }

  @Override
  public Request request() {
    return new Request.Builder().url(this.testUrl).build();
  }

  @Override
  public Timeout timeout() {
    return null;
  }
}
