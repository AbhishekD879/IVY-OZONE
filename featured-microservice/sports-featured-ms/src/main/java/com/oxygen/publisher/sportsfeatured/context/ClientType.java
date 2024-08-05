package com.oxygen.publisher.sportsfeatured.context;

import java.util.Arrays;
import java.util.Optional;
import org.apache.commons.lang3.StringUtils;

public enum ClientType {
  // for now we don't use client type parameter for web client in socket connection
  ANDROID("android"),
  IOS("ios"),
  WEB(null),
  WP("wp");

  private String type;

  ClientType(String type) {
    this.type = type;
  }

  public static ClientType from(String type) {
    Optional<ClientType> optionalClientType =
        Arrays.stream(ClientType.values())
            .filter(clientType -> StringUtils.equals(clientType.getType(), type))
            .findFirst();
    return optionalClientType.orElseThrow(
        () -> new IllegalArgumentException("Client type: " + type + " not recognized."));
  }

  public String getType() {
    return type;
  }

  public String getTypeInUrlForm() {
    return Optional.ofNullable(type).map(value -> "/" + value).orElse("");
  }
}
