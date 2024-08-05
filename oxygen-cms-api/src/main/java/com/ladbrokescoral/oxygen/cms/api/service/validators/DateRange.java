package com.ladbrokescoral.oxygen.cms.api.service.validators;

import java.lang.annotation.Documented;
import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;
import javax.validation.Constraint;
import javax.validation.Payload;

@Documented
@Constraint(validatedBy = DateRangeValidator.class)
@Target({ElementType.TYPE})
@Retention(RetentionPolicy.RUNTIME)
public @interface DateRange {

  String startDateField();

  String endDateField();

  String message() default "Start date must be before end date";

  Class<?>[] groups() default {};

  Class<? extends Payload>[] payload() default {};
}
