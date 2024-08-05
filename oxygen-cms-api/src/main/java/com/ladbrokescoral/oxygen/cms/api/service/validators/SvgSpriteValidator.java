package com.ladbrokescoral.oxygen.cms.api.service.validators;

import com.ladbrokescoral.oxygen.cms.api.entity.SvgSprite;
import java.util.stream.Stream;
import javax.validation.ConstraintValidator;
import javax.validation.ConstraintValidatorContext;
import lombok.extern.slf4j.Slf4j;

@Slf4j
public class SvgSpriteValidator implements ConstraintValidator<ValidSvgSprite, String> {

  @Override
  public void initialize(ValidSvgSprite constraintAnnotation) {
    // nothing to initialize so it's empty but requires to be overwritten
  }

  @Override
  public boolean isValid(String value, ConstraintValidatorContext context) {
    if (value != null) {
      return Stream.of(SvgSprite.values()).anyMatch(s -> s.getSpriteName().equals(value));
    }
    return true;
  }
}
