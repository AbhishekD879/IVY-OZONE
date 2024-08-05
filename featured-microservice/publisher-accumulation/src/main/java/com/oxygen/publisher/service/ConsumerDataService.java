package com.oxygen.publisher.service;

import com.newrelic.api.agent.NewRelic;
import com.oxygen.health.api.ReloadableService;
import java.io.IOException;
import java.util.Objects;
import java.util.function.Consumer;
import lombok.extern.slf4j.Slf4j;
import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

@Slf4j
public class ConsumerDataService implements ReloadableService {

  private boolean isOnService;
  private boolean healthStatusForExternal;

  protected <R> Callback<R> doCall(Consumer<R> onSuccess) {
    return new Callback<R>() {
      @Override
      public void onResponse(Call<R> call, Response<R> response) {
        processResponse(response, onSuccess);
      }

      @Override
      public void onFailure(Call<R> call, Throwable throwable) {
        processFailure(call, throwable, onSuccess);
      }
    };
  }

  protected <R> void processResponse(Response<R> response, Consumer<R> onSuccess) {
    // got response from consumer, so no need to restart container as no issues from publisher side
    healthStatusForExternal = true;
    if (response.isSuccessful() && !Objects.isNull(response.body())) {
      onSuccess.accept(response.body());
      isOnService = true;
    } else {
      try {
        log.error(
            "Got error response from consumer: code->'{}', errorBody->'{}', body->'{}'",
            response.code(),
            response.errorBody().string(),
            response.body());
        onSuccess.accept(null);
        NewRelic.noticeError(
            "Got error code " + response.code() + " " + response.raw().request().url());
      } catch (IOException e) {
        log.error("Error during error handling. Can't parse error response ", e);
        NewRelic.noticeError(e);
      } finally {
        isOnService = false;
      }
    }
  }

  protected <R> void processFailure(Call call, Throwable throwable, Consumer<R> onFailure) {
    log.error(
        "[{}] Connection failed on middleware call. ", call.request().url().toString(), throwable);
    NewRelic.noticeError(throwable);
    isOnService = false;
    healthStatusForExternal = false;
    onFailure.accept(null);
  }

  @Override
  public void start() {
    isOnService = true;
  }

  @Override
  public void evict() {
    isOnService = false;
  }

  @Override
  public boolean isHealthy() {
    return isOnService;
  }

  @Override
  public void onFail(Exception ex) {
    log.error("Failed on middleware call.", ex);
    NewRelic.noticeError(ex);
    isOnService = false;
  }

  @Override
  public boolean getHealthStatusForExternal() {
    return healthStatusForExternal;
  }
}
