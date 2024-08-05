package com.ladbrokescoral.oxygen.cms.api.entity.onboarding;

import java.time.Instant;
import lombok.Data;
import lombok.EqualsAndHashCode;
import org.springframework.data.mongodb.core.mapping.Document;

@Data
@EqualsAndHashCode(callSuper = true)
@Document("coupon-stats-widget")
public class CouponStatsWidget extends OnBoarding {

  private String buttonText;
  private Instant displayFrom;
  private Instant displayTo;
}
