package com.ladbrokescoral.oxygen.cms.api.service.validators;

import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;
import javax.validation.Constraint;
import javax.validation.Payload;

@Constraint(validatedBy = ImageFileTypeValidator.class)
@Target({ElementType.PARAMETER, ElementType.FIELD})
@Retention(RetentionPolicy.RUNTIME)
public @interface ValidFileType {

  String[] value();

  String message() default "Not supported image type ";

  Class<?>[] groups() default {};

  Class<? extends Payload>[] payload() default {};
}
