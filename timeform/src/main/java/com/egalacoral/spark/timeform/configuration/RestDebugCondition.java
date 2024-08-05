package com.egalacoral.spark.timeform.configuration;

import org.springframework.context.annotation.Condition;
import org.springframework.context.annotation.ConditionContext;
import org.springframework.core.type.AnnotatedTypeMetadata;

public class RestDebugCondition implements Condition {

  private static final String DEBUG_PROPERTY_NAME = "rest.debug";

  @Override
  public boolean matches(ConditionContext context, AnnotatedTypeMetadata metadata) {
    return context.getEnvironment().containsProperty(DEBUG_PROPERTY_NAME) //
        && Boolean.TRUE
            .toString()
            .equalsIgnoreCase(context.getEnvironment().getProperty(DEBUG_PROPERTY_NAME).trim());
  }
}
