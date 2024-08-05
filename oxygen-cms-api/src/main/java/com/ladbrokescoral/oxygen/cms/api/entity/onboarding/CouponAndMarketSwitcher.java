package com.ladbrokescoral.oxygen.cms.api.entity.onboarding;

import lombok.Data;
import lombok.EqualsAndHashCode;
import org.springframework.data.mongodb.core.mapping.Document;

@Data
@EqualsAndHashCode(callSuper = true)
@Document("couponAndMarketSwitcher")
public class CouponAndMarketSwitcher extends OnBoarding {
  private String buttonText;
}
