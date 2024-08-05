package com.ladbrokescoral.oxygen.cms.api.service.validators;

import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;
import javax.validation.Constraint;
import javax.validation.Payload;
import org.springframework.core.annotation.AliasFor;

@Constraint(validatedBy = ImageFileSizeValidator.class)
@Target(ElementType.PARAMETER)
@Retention(RetentionPolicy.RUNTIME)
public @interface ValidFileSize {

  @AliasFor("max")
  long value() default Long.MAX_VALUE;

  long min() default 0;

  @AliasFor("value")
  long max() default Long.MAX_VALUE;

  String message() default "Not supported image size ";

  Class<?>[] groups() default {};

  Class<? extends Payload>[] payload() default {};
}
