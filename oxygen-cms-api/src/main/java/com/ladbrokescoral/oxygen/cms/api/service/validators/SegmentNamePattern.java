package com.ladbrokescoral.oxygen.cms.api.service.validators;

import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;
import javax.validation.Constraint;
import javax.validation.Payload;
import javax.validation.ReportAsSingleViolation;
import javax.validation.constraints.NotBlank;
import javax.validation.constraints.NotNull;

@Constraint(validatedBy = SegmentValidator.class)
@Target({
  ElementType.METHOD,
  ElementType.FIELD,
  ElementType.CONSTRUCTOR,
  ElementType.PARAMETER,
  ElementType.TYPE_PARAMETER,
  ElementType.TYPE_USE
})
@Retention(RetentionPolicy.RUNTIME)
@ReportAsSingleViolation
@NotNull
@NotBlank
public @interface SegmentNamePattern {

  String message() default "Not a valid segment name";

  Class<?>[] groups() default {};

  Class<? extends Payload>[] payload() default {};
}
