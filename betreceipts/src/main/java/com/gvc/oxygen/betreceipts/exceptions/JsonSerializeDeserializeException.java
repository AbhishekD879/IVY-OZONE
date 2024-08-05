package com.gvc.oxygen.betreceipts.exceptions;

public class JsonSerializeDeserializeException extends RuntimeException {
  public JsonSerializeDeserializeException(String msg, Throwable rootCause) {
    super(msg, rootCause);
  }
}
