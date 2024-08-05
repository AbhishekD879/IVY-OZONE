package com.ladbrokescoral.oxygen.cms.api.service.validators;

import java.time.temporal.Temporal;
import javax.validation.ConstraintValidator;
import javax.validation.ConstraintValidatorContext;
import javax.validation.ValidationException;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.BeanWrapper;
import org.springframework.beans.BeanWrapperImpl;

@Slf4j
public class DateRangeValidator implements ConstraintValidator<DateRange, Object> {

  private String startDateField;
  private String endDateField;

  @Override
  public void initialize(DateRange constraintAnnotation) {
    this.startDateField = constraintAnnotation.startDateField();
    this.endDateField = constraintAnnotation.endDateField();
  }

  @Override
  public boolean isValid(Object bean, ConstraintValidatorContext context) {

    BeanWrapper beanWrapper = new BeanWrapperImpl(bean);

    Object startDate = beanWrapper.getPropertyValue(startDateField);
    Object endDate = beanWrapper.getPropertyValue(endDateField);

    if (startDate == null || endDate == null) {
      return true;
    }
    if (!startDate.getClass().equals(endDate.getClass())) {
      throw new ValidationException(
          "startDateField and endDateField have to be of the same type for Date Range validation");
    }

    if (startDate instanceof Temporal) {
      return isTemporalValid(startDate, endDate);
    }

    throw new ValidationException(
        String.format(
            "%s type is not supported for Date Range validation", startDate.getClass().getName()));
  }

  private boolean isTemporalValid(Object rawStartDate, Object rawEndDate) {

    Temporal startDate = (Temporal) rawStartDate;
    Temporal endDate = (Temporal) rawEndDate;

    if (startDate instanceof Comparable) {
      return ((Comparable<Temporal>) startDate).compareTo(endDate) < 0;
    }
    throw new ValidationException(
        String.format(
            "%s type is not supported for Date Range validation", startDate.getClass().getName()));
  }
}
