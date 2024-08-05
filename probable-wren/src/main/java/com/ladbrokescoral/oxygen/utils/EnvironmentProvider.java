package com.ladbrokescoral.oxygen.utils;

import org.springframework.core.env.Environment;

public class EnvironmentProvider {

  private final Environment environment;

  public EnvironmentProvider(Environment environment) {
    this.environment = environment;
  }

  public String getEnvironmentVariable(String variable) {
    return environment.getProperty(variable);
  }
}
