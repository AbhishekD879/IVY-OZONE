package com.ladbrokescoral.oxygen.cms.api.service;

import static org.assertj.core.api.AssertionsForClassTypes.assertThatThrownBy;
import static org.mockito.Mockito.never;
import static org.mockito.Mockito.verify;

import com.ladbrokescoral.oxygen.cms.api.entity.CouponSegment;
import com.ladbrokescoral.oxygen.cms.api.repository.CouponSegmentRepository;
import java.time.DayOfWeek;
import java.time.Duration;
import java.time.Instant;
import java.util.EnumSet;
import java.util.UUID;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;

@RunWith(MockitoJUnitRunner.class)
public class CouponSegmentServiceTest {

  @Mock private CouponSegmentRepository couponSegmentRepository;

  @InjectMocks private CouponSegmentService couponSegmentService;

  @Test
  public void saveDatesAreSet() {
    CouponSegment couponSegment = couponSegment();

    couponSegment.setFrom(Instant.now());
    couponSegment.setTo(Instant.now().plus(Duration.ofDays(7)));

    couponSegmentService.save(couponSegment);

    verify(couponSegmentRepository).save(couponSegment);
  }

  @Test
  public void saveWeekIsSet() {
    CouponSegment couponSegment = couponSegment();

    EnumSet<DayOfWeek> days = EnumSet.of(DayOfWeek.THURSDAY);
    couponSegment.setDayOfWeek(days);

    couponSegmentService.save(couponSegment);

    verify(couponSegmentRepository).save(couponSegment);
  }

  @Test
  public void saveNeitherWeekNorDatesAreSet() {
    CouponSegment couponSegment = couponSegment();

    assertThatThrownBy(() -> couponSegmentService.save(couponSegment))
        .isInstanceOf(IllegalArgumentException.class)
        .hasMessage("Properties 'to', 'from' must not be nulls");

    verify(couponSegmentRepository, never()).save(couponSegment);
  }

  @Test
  public void saveWeekNotSetAndEndDateIsMissing() {
    CouponSegment couponSegment = couponSegment();
    couponSegment.setFrom(Instant.now());

    assertThatThrownBy(() -> couponSegmentService.save(couponSegment))
        .isInstanceOf(IllegalArgumentException.class)
        .hasMessage("Properties 'to', 'from' must not be nulls");

    verify(couponSegmentRepository, never()).save(couponSegment);
  }

  @Test
  public void saveBothWeekAndDatesAreSet() {
    CouponSegment couponSegment = couponSegment();

    couponSegment.setFrom(Instant.now());
    couponSegment.setTo(Instant.now().plus(Duration.ofDays(5)));

    EnumSet<DayOfWeek> days = EnumSet.of(DayOfWeek.THURSDAY);
    couponSegment.setDayOfWeek(days);

    assertThatThrownBy(() -> couponSegmentService.save(couponSegment))
        .isInstanceOf(IllegalArgumentException.class)
        .hasMessage("Properties 'to', 'from' must be nulls when 'dayOfWeek' is specified");

    verify(couponSegmentRepository, never()).save(couponSegment);
  }

  private CouponSegment couponSegment() {
    CouponSegment couponSegment = new CouponSegment();

    couponSegment.setId(UUID.randomUUID().toString());
    couponSegment.setBrand("brand");
    couponSegment.setCouponKeys("3,8,46");
    couponSegment.setTitle("title");
    couponSegment.setSortOrder(0.0);

    return couponSegment;
  }
}
