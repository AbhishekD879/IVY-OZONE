package com.ladbrokescoral.oxygen.cms.util;

import com.ladbrokescoral.oxygen.cms.api.entity.BetPackToken;
import java.util.List;
import javax.validation.ConstraintValidator;
import javax.validation.ConstraintValidatorContext;

public class BetTokenValidator implements ConstraintValidator<BetToken, List<BetPackToken>> {

  @Override
  public boolean isValid(
      List<BetPackToken> list, ConstraintValidatorContext constraintValidatorContext) {
    return (null != list && !list.isEmpty() && !list.contains(null));
  }
}
