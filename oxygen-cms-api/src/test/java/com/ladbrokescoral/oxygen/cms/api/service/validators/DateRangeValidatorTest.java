package com.ladbrokescoral.oxygen.cms.api.service.validators;

import static org.assertj.core.api.AssertionsForClassTypes.assertThatThrownBy;
import static org.junit.Assert.assertFalse;
import static org.junit.Assert.assertTrue;

import java.time.Duration;
import java.time.Instant;
import java.time.LocalDate;
import java.time.LocalDateTime;
import java.util.Date;
import java.util.stream.Stream;
import javax.validation.ConstraintValidatorContext;
import javax.validation.ValidationException;
import lombok.Data;
import lombok.experimental.Accessors;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;

// FIXME: we are using Instant. Review, Rework, Remove.
@RunWith(MockitoJUnitRunner.class)
public class DateRangeValidatorTest {

  @Mock private ConstraintValidatorContext validatorContext;

  private DateRange InstantDateRange = dateRangeMockFor(InstantTestBean.class);
  private DateRange localDateTimeRange = dateRangeMockFor(LocalDateTimeTestBean.class);
  private DateRange localDateRange = dateRangeMockFor(LocalDateTestBean.class);
  private DateRange incompatibleTypesDateRange = dateRangeMockFor(IncompatibleTypesTestBean.class);
  private DateRange unsupportedTypeDateRange = dateRangeMockFor(UnsupportedTypeTestBean.class);

  private final DateRangeValidator dateRangeValidator = new DateRangeValidator();

  @Test
  public void validInstantDateRange() {
    dateRangeValidator.initialize(InstantDateRange);

    Instant now = Instant.now();
    InstantTestBean InstantDateTestBean =
        new InstantTestBean()
            .setInstantStartDate(now)
            .setInstantEndDate(now.plus(Duration.ofDays(5)));

    assertTrue(dateRangeValidator.isValid(InstantDateTestBean, validatorContext));
  }

  @Test
  public void invalidInstantDateRange() {
    dateRangeValidator.initialize(InstantDateRange);

    Instant now = Instant.now();
    InstantTestBean InstantDateTestBean =
        new InstantTestBean()
            .setInstantStartDate(now.plus(Duration.ofDays(9)))
            .setInstantEndDate(now.plus(Duration.ofDays(5)));

    assertFalse(dateRangeValidator.isValid(InstantDateTestBean, validatorContext));
  }

  @Test
  public void zeroDifferenceInstantDateRange() {
    dateRangeValidator.initialize(InstantDateRange);

    Instant now = Instant.now();
    InstantTestBean InstantDateTestBean =
        new InstantTestBean().setInstantStartDate(now).setInstantEndDate(now);

    assertFalse(dateRangeValidator.isValid(InstantDateTestBean, validatorContext));
  }

  @Test
  public void validLocalDateTimeRange() {
    dateRangeValidator.initialize(localDateTimeRange);

    LocalDateTime now = LocalDateTime.now();
    LocalDateTimeTestBean localDateTimeTestBean =
        new LocalDateTimeTestBean()
            .setStartLocalDateTime(now)
            .setEndLocalDateTime(now.plusSeconds(43));

    assertTrue(dateRangeValidator.isValid(localDateTimeTestBean, validatorContext));
  }

  @Test
  public void invalidLocalDateTimeRange() {
    dateRangeValidator.initialize(localDateTimeRange);

    LocalDateTime now = LocalDateTime.now();
    LocalDateTimeTestBean localDateTimeTestBean =
        new LocalDateTimeTestBean()
            .setStartLocalDateTime(now)
            .setEndLocalDateTime(now.minusMinutes(12));

    assertFalse(dateRangeValidator.isValid(localDateTimeTestBean, validatorContext));
  }

  @Test
  public void zeroDifferenceLocalDateTimeRange() {
    dateRangeValidator.initialize(localDateTimeRange);

    LocalDateTime now = LocalDateTime.now();
    LocalDateTimeTestBean localDateTimeTestBean =
        new LocalDateTimeTestBean().setStartLocalDateTime(now).setEndLocalDateTime(now);

    assertFalse(dateRangeValidator.isValid(localDateTimeTestBean, validatorContext));
  }

  @Test
  public void validLocalDateRange() {
    dateRangeValidator.initialize(localDateRange);

    LocalDate now = LocalDate.now();
    LocalDateTestBean localDateTestBean =
        new LocalDateTestBean().setStartLocalDate(now).setEndLocalDate(now.plusDays(21));

    assertTrue(dateRangeValidator.isValid(localDateTestBean, validatorContext));
  }

  @Test
  public void invalidLocalDateRange() {
    dateRangeValidator.initialize(localDateRange);

    LocalDate now = LocalDate.now();
    LocalDateTestBean localDateTestBean =
        new LocalDateTestBean().setStartLocalDate(now.plusDays(2)).setEndLocalDate(now.plusDays(1));

    assertFalse(dateRangeValidator.isValid(localDateTestBean, validatorContext));
  }

  @Test
  public void zeroDifferenceLocalDateRange() {
    dateRangeValidator.initialize(localDateRange);

    LocalDate now = LocalDate.now();
    LocalDateTestBean localDateTestBean =
        new LocalDateTestBean().setStartLocalDate(now.plusDays(3)).setEndLocalDate(now.plusDays(3));

    assertFalse(dateRangeValidator.isValid(localDateTestBean, validatorContext));
  }

  @Test
  public void isValidIfBothAreNulls() {
    dateRangeValidator.initialize(localDateRange);

    LocalDateTestBean localDateTestBean = new LocalDateTestBean();

    assertTrue(dateRangeValidator.isValid(localDateTestBean, validatorContext));
  }

  @Test
  public void isValidIfEitherNull() {
    dateRangeValidator.initialize(localDateRange);

    LocalDateTestBean localDateTestBean = new LocalDateTestBean().setEndLocalDate(LocalDate.now());

    assertTrue(dateRangeValidator.isValid(localDateTestBean, validatorContext));
  }

  @Test
  public void incompatibleTypes() {
    dateRangeValidator.initialize(incompatibleTypesDateRange);

    IncompatibleTypesTestBean incompatibleTypesTestBean =
        new IncompatibleTypesTestBean().setStartLocalDate(LocalDate.now()).setIncompatibleType(777);

    assertThatThrownBy(
            () -> dateRangeValidator.isValid(incompatibleTypesTestBean, validatorContext))
        .isInstanceOf(ValidationException.class)
        .hasMessage(
            "startDateField and endDateField have to be of the same type for Date Range validation");
  }

  @Test
  public void unsupportedType() {
    dateRangeValidator.initialize(unsupportedTypeDateRange);

    Instant now = Instant.now();
    UnsupportedTypeTestBean unsupportedTypeTestBean =
        new UnsupportedTypeTestBean()
            .setUnsupportedStartDate(Date.from(now))
            .setUnsupportedEndDate(Date.from(Instant.now().plus(Duration.ofDays(3))));

    assertThatThrownBy(() -> dateRangeValidator.isValid(unsupportedTypeTestBean, validatorContext))
        .isInstanceOf(ValidationException.class)
        .hasMessage("java.util.Date type is not supported for Date Range validation");
  }

  private DateRange dateRangeMockFor(Class<?> beanType) {
    return Stream.of(beanType.getDeclaredAnnotations())
        .filter(annotation -> annotation.annotationType().equals(DateRange.class))
        .findFirst()
        .map(DateRange.class::cast)
        .orElseThrow(
            () ->
                new IllegalArgumentException(
                    String.format("%s does not have DateRange on it", beanType.getName())));
  }

  @Data
  @Accessors(chain = true)
  @DateRange(startDateField = "instantStartDate", endDateField = "instantEndDate")
  private static class InstantTestBean {
    Instant instantStartDate;
    Instant instantEndDate;
  }

  @Data
  @Accessors(chain = true)
  @DateRange(startDateField = "startLocalDateTime", endDateField = "endLocalDateTime")
  private static class LocalDateTimeTestBean {
    LocalDateTime startLocalDateTime;
    LocalDateTime endLocalDateTime;
  }

  @Data
  @Accessors(chain = true)
  @DateRange(startDateField = "startLocalDate", endDateField = "endLocalDate")
  private static class LocalDateTestBean {
    LocalDate startLocalDate;
    LocalDate endLocalDate;
  }

  @Data
  @Accessors(chain = true)
  @DateRange(startDateField = "startLocalDate", endDateField = "incompatibleType")
  private static class IncompatibleTypesTestBean {
    LocalDate startLocalDate;
    Number incompatibleType;
  }

  @Data
  @Accessors(chain = true)
  @DateRange(startDateField = "unsupportedStartDate", endDateField = "unsupportedEndDate")
  private static class UnsupportedTypeTestBean {
    Date unsupportedStartDate;
    Date unsupportedEndDate;
  }
}
