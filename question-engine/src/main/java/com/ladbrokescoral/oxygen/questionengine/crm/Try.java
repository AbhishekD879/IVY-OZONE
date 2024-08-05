package com.ladbrokescoral.oxygen.questionengine.crm;

import lombok.extern.slf4j.Slf4j;

import java.util.function.Function;
import java.util.function.Supplier;
@Slf4j
class Try<T> {
  private T value;
  private Exception exception;

  private Try() {}

  public T getResponse() {
    return this.value;
  }

  private void setValue(T value) {
    this.value = value;
  }

  public boolean hasError() {
    return this.exception != null;
  }

  private void setException(Exception exception) {
    this.exception = exception;
  }

  public T orElseThrow(Function<String,RuntimeException> exceptionCall) {
    if (this.exception != null) {
      log.error("CRM Award-API orElseThrow {}",exception.getMessage());
      RuntimeException runtimeException = exceptionCall.apply(exception.getMessage());
      runtimeException.addSuppressed(this.exception);
      throw runtimeException;
    } else {
      return this.value;
    }
  }

  public static <K> Try<K> of(SupplierWithException<K, Exception> responseCall) {
    Try<K> responseTry = new Try<>();
    try {
      responseTry.setValue(responseCall.get());
    } catch (Exception var3) {
      responseTry.setException(var3);
    }
    return responseTry;
  }
}
