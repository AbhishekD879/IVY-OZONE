package com.entain.oxygen.util;

public enum KafkaConstant {
  SSL_ENABLED_PROTOCOLS("ssl.enabled.protocols"),
  SSL_ENABLED_PROTOCOLS_VERSIONS("TLSv1.2,TLSv1.1,TLSv1"),
  SSL_ENDPOINT_IDENTIFICATION_ALGORITHM("ssl.endpoint.identification.algorithm"),
  EMPTY_STRING("");

  private final String value;

  KafkaConstant(String value) {
    this.value = value;
  }

  public String value() {
    return this.value;
  }
}
