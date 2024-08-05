package com.ladbrokescoral.oxygen.cms.api.controller.dto;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.ladbrokescoral.oxygen.cms.api.controller.dto.onboarding.CouponAndMarketSwitcherDto;
import lombok.Data;

@Data
@JsonIgnoreProperties(
    value = {
      "displayFrom",
      "displayTo",
      "id",
      "createdBy",
      "createdByUserName",
      "updatedAt",
      "updatedBy",
      "updatedByUserName",
      "createdAt"
    })
public class CouponAndMarketSwitcherCFDto extends CouponAndMarketSwitcherDto {}
