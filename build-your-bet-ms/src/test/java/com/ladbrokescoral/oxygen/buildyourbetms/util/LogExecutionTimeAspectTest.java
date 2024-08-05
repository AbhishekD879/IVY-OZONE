package com.ladbrokescoral.oxygen.buildyourbetms.util;

import org.assertj.core.api.Assertions;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.boot.test.context.runner.ApplicationContextRunner;

public class LogExecutionTimeAspectTest {

  private ApplicationContextRunner applicationRunner;

  @BeforeEach
  public void init() {
    applicationRunner = new ApplicationContextRunner();
  }

  @Test
  public void testForPresenceOfBean() {

    this.applicationRunner
        .withUserConfiguration(LogExecutionTimeAspect.class)
        .withPropertyValues("byb.log.execution.time.enabled=true")
        .run(
            context -> {
              Assertions.assertThat(context).hasSingleBean(LogExecutionTimeAspect.class);
            });
  }

  @Test
  public void testForAbsenceOfBean() {
    this.applicationRunner
        .withUserConfiguration(LogExecutionTimeAspect.class)
        .withPropertyValues("byb.log.execution.time.enabled=false")
        .run(
            context -> {
              Assertions.assertThat(context).doesNotHaveBean(LogExecutionTimeAspect.class);
            });
  }
}
