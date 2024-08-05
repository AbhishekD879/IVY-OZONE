package com.coral.oxygen.middleware.ms.quickbet.connector;

import lombok.Value;

/**
 * This is just a simple wrapper, mainly used to wrap a basic String response to provide that a
 * valid JSON will be return (returned pure String is not a proper JSON).
 */
@Value
public class BasicResponse {
  private String message;
}
