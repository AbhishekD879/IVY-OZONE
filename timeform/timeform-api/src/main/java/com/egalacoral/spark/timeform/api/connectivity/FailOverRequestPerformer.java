package com.egalacoral.spark.timeform.api.connectivity;

import com.egalacoral.spark.timeform.api.DataCallback;
import com.egalacoral.spark.timeform.api.TimeFormException;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import retrofit2.Call;

public class FailOverRequestPerformer implements RequestPerformer {

  private static final Logger LOGGER = LoggerFactory.getLogger(FailOverRequestPerformer.class);

  private final RequestPerformer delegate;

  private final FailOverStrategy failOverStrategy;

  private final Runnable reloginAction;

  public FailOverRequestPerformer(
      RequestPerformer delegate, FailOverStrategy failOverStrategy, Runnable reloginAction) {
    this.delegate = delegate;
    this.failOverStrategy = failOverStrategy;
    this.reloginAction = reloginAction;
  }

  @Override
  public <T> T invokeSync(Call<T> call) {
    T result = null;
    int counter = 0;
    boolean retry;
    do {
      retry = false;
      try {
        result = delegate.invokeSync(call);
      } catch (Exception e) {
        counter++;
        FailOverStrategy.FailOverAction action =
            failOverStrategy.onError(convertEception(e), counter);
        if (FailOverStrategy.FailOverAction.RELOGIN_AND_RETRY.equals(action)) {
          relogin();
        }
        if (FailOverStrategy.FailOverAction.RELOGIN_AND_RETRY.equals(action) //
            || FailOverStrategy.FailOverAction.RETRY.equals(action)) {
          LOGGER.warn("Sync retry requested. {}", counter);
          retry = true;
          call = call.clone();
        } else {
          throw convertEception(e);
        }
      }
    } while (retry);
    return result;
  }

  private void relogin() {
    boolean retry;
    int counter = 0;
    do {
      retry = false;
      try {
        reloginAction.run();
      } catch (Exception e) {
        counter++;
        FailOverStrategy.FailOverAction action =
            failOverStrategy.onReloginError(convertEception(e), counter);
        if (FailOverStrategy.FailOverAction.RELOGIN_AND_RETRY.equals(action) //
            || FailOverStrategy.FailOverAction.RETRY.equals(action)) {
          retry = true;
          try {
            // TODO relogin timeout
            Thread.sleep(1000);
          } catch (InterruptedException ex) {
            LOGGER.error("Relogin failed", ex);
            Thread.currentThread().interrupt();
          }
          LOGGER.warn("Relogin requested. {}", counter);
        } else {
          throw convertEception(e);
        }
      }
    } while (retry);
  }

  @Override
  public <T> void invokeAsync(Call<T> call, DataCallback<T> dataCallback) {
    FailOverCallback foCallback = new FailOverCallback<>(dataCallback, call);
    try {
      delegate.invokeAsync(call, foCallback);
    } catch (Exception e) {
      foCallback.onError(convertEception(e));
    }
  }

  private TimeFormException convertEception(Throwable throwable) {
    TimeFormException tfe;
    if (throwable instanceof TimeFormException) {
      tfe = (TimeFormException) throwable;
    } else {
      tfe = new TimeFormException(throwable);
    }
    return tfe;
  }

  private class FailOverCallback<T> implements DataCallback<T> {

    private final DataCallback<T> delegate;

    private final Call<T> call;

    private int counter = 0;

    public FailOverCallback(DataCallback<T> delegate, Call<T> call) {
      this.delegate = delegate;
      this.call = call;
    }

    @Override
    public void onResponse(T data) {
      delegate.onResponse(data);
    }

    @Override
    public void onError(Exception exeption) {
      try {
        counter++;
        FailOverStrategy.FailOverAction action =
            failOverStrategy.onError(convertEception(exeption), counter);
        if (FailOverStrategy.FailOverAction.RELOGIN_AND_RETRY.equals(action)) {
          relogin();
        }
        if (FailOverStrategy.FailOverAction.RELOGIN_AND_RETRY.equals(action) //
            || FailOverStrategy.FailOverAction.RETRY.equals(action)) {
          LOGGER.warn("Async retry requested. {}", counter);
          retryRelogin();
        } else {
          delegate.onError(exeption);
        }
      } catch (Exception e) {
        delegate.onError(e);
      }
    }

    private void retryRelogin() {
      try {
        FailOverRequestPerformer.this.delegate.invokeAsync(call.clone(), this);
      } catch (Exception e) {
        this.onError(convertEception(e));
      }
    }
  }
}
