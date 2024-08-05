package com.coral.oxygen.middleware.pojos.model;

import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;

@Target(value = ElementType.METHOD)
@Retention(value = RetentionPolicy.RUNTIME)
public @interface ChangeDetect {

  boolean compareNestedObject() default false;

  boolean compareCollection() default false;

  boolean compareList() default false;

  boolean minor() default false;
}
