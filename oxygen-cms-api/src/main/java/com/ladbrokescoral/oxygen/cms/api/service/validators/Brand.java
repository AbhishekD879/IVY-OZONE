package com.ladbrokescoral.oxygen.cms.api.service.validators;

import static java.lang.annotation.ElementType.CONSTRUCTOR;
import static java.lang.annotation.ElementType.FIELD;
import static java.lang.annotation.ElementType.METHOD;
import static java.lang.annotation.ElementType.PARAMETER;

import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;
import javax.validation.Constraint;
import javax.validation.Payload;
import javax.validation.ReportAsSingleViolation;
import javax.validation.constraints.NotBlank;
import javax.validation.constraints.NotNull;

@Constraint(validatedBy = BrandValidator.class)
@Target({METHOD, FIELD, CONSTRUCTOR, PARAMETER})
@Retention(RetentionPolicy.RUNTIME)
@ReportAsSingleViolation
@NotNull
@NotBlank
public @interface Brand {

  String message() default "Not supported brand code. Please add brand with such code.";

  Class<?>[] groups() default {};

  Class<? extends Payload>[] payload() default {};
}
