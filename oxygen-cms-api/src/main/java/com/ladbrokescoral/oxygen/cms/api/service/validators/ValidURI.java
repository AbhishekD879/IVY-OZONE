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
import javax.validation.constraints.NotEmpty;
import javax.validation.constraints.Pattern;

@Target({METHOD, FIELD, CONSTRUCTOR, PARAMETER})
@Retention(RetentionPolicy.RUNTIME)
@NotEmpty
@Constraint(validatedBy = {})
@Pattern(regexp = "[^/]*", message = "should not contain '/' character.")
public @interface ValidURI {

  String message() default "should not contain '/' character.";

  Class<?>[] groups() default {};

  Class<? extends Payload>[] payload() default {};
}
