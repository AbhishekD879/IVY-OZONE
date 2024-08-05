package com.coral.oxygen.middleware.ms.quickbet.connector.dto.request.v2;

/** Created by azayats on 23.11.17. */
public interface RequestValidator<T> {

  void validate(T request) throws RequestValidationException;
}
