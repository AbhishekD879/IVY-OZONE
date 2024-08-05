package com.ladbrokescoral.oxygen.cms.api.dto;

import java.time.DayOfWeek;
import java.time.Instant;
import java.util.EnumSet;
import lombok.Data;
import org.springframework.data.annotation.Id;

@Data
public class CouponSegmentDto {
  @Id private String id;
  private String title;
  private String couponKeys;
  private EnumSet<DayOfWeek> dayOfWeek;
  private Instant from;
  private Instant to;
}
