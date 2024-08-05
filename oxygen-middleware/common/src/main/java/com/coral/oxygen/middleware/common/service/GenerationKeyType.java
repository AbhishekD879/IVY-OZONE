package com.coral.oxygen.middleware.common.service;

public enum GenerationKeyType {
  FEATURED_GENERATION("featured_generation"),
  INPLAY_GENERATION("inplay_generation");

  private String key;

  GenerationKeyType(String key) {
    this.key = key;
  }

  public String getKey() {
    return key;
  }
}
