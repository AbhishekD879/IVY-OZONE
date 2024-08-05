package com.coral.oxygen.middleware.common.imdg;

public enum DistributedProvider {
  HAZELCAST("hazelcast"),
  REDIS_TEMPLATE("redis_template");

  String name;

  DistributedProvider(String name) {
    this.name = name;
  }

  public String getName() {
    return name;
  }
}
