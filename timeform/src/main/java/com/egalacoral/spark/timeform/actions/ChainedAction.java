package com.egalacoral.spark.timeform.actions;

import com.egalacoral.spark.timeform.api.DataCallback;
import java.util.function.Consumer;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class ChainedAction {

  private static final transient Logger LOGGER = LoggerFactory.getLogger(ChainedAction.class);

  private Consumer<DataCallbackWrapper> action;

  private Consumer<Exception> onError;

  private Runnable onSuccess;

  private ChainedAction after;

  private volatile boolean asyncMode = false;

  private volatile boolean delegated = false;

  public ChainedAction() {
    onSuccess = () -> {};
    onError = (e) -> {};
  }

  public void setAction(Consumer<DataCallbackWrapper> action) {
    this.action = action;
  }

  public void call() {
    callOwnAction();
  }

  protected void setDelegated(boolean delegated) {
    this.delegated = delegated;
  }

  protected void setAsyncMode(boolean mode) {
    this.asyncMode = mode;
  }

  protected void fireOnError(Exception e) {
    this.onError.accept(e);
  }

  protected void fireOnSuccess() {
    this.onSuccess.run();
  }

  protected void callOwnAction() {
    try {
      action.accept(
          new DataCallbackWrapper() {
            @Override
            public <T> DataCallback<T> wrap(DataCallback<T> originalCallback) {
              asyncMode = true;
              return new DataCallback<T>() {
                @Override
                public void onResponse(T data) {
                  try {
                    originalCallback.onResponse(data);
                  } finally {
                    onSuccess.run();
                  }
                }

                @Override
                public void onError(Exception throwable) {
                  try {
                    originalCallback.onError(throwable);
                  } finally {
                    onError.accept(throwable);
                  }
                }
              };
            }
          });

      if (!asyncMode && !delegated) {
        onSuccess.run();
      }
    } catch (Exception e) {
      LOGGER.error("", e);
      onError.accept(e);
    }
  }

  public void addOnSuccess(Runnable onSuccess) {
    Runnable oldSuccess = this.onSuccess;
    this.onSuccess =
        () -> {
          try {
            oldSuccess.run();
          } finally {
            onSuccess.run();
          }
        };
  }

  public void addOnError(Consumer<Exception> onError) {
    Consumer<Exception> oldError = this.onError;
    this.onError =
        e -> {
          try {
            oldError.accept(e);
          } finally {
            onError.accept(e);
          }
        };
  }

  public void setAfter(ChainedAction after) {
    if (this.after != null) {
      throw new IllegalStateException("After already configured");
    }
    this.after = after;
    this.addOnSuccess(
        () -> {
          this.after.call();
        });
    this.addOnError(after::fireOnError);
  }

  protected void delegate(ChainedAction delegate) {
    delegate.addOnSuccess(this::fireOnSuccess);

    delegate.addOnError(this::fireOnError);

    delegated = true;
    delegate.call();
  }
}
