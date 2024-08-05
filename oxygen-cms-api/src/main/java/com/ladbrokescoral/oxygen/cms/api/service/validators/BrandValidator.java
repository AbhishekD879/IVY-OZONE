package com.ladbrokescoral.oxygen.cms.api.service.validators;

import com.ladbrokescoral.oxygen.cms.api.service.BrandService;
import javax.validation.ConstraintValidator;
import javax.validation.ConstraintValidatorContext;
import org.springframework.beans.factory.annotation.Autowired;

public class BrandValidator implements ConstraintValidator<Brand, String> {

  @Autowired private BrandService brandService;

  @Override
  public void initialize(Brand constraintAnnotation) {
    // nothing
  }

  @Override
  public boolean isValid(String value, ConstraintValidatorContext context) {
    return com.ladbrokescoral.oxygen.cms.api.entity.Brand.BRAND_LIST.contains(value)
        || brandService.findByBrandCode(value).isPresent();
  }
}
