package com.ladbrokescoral.oxygen.cms.api.service.validators;

import java.util.regex.Pattern;
import javax.validation.ConstraintValidator;
import javax.validation.ConstraintValidatorContext;

public class SegmentValidator implements ConstraintValidator<SegmentNamePattern, String> {

  private static final Pattern SEGMENT_PATTERN = Pattern.compile("^([a-zA-Z0-9_-])+$");

  @Override
  public void initialize(SegmentNamePattern constraintAnnotation) {
    // nothing
  }

  @Override
  public boolean isValid(String value, ConstraintValidatorContext context) {
    return SEGMENT_PATTERN.matcher(value).matches();
  }
}
