package com.ladbrokescoral.oxygen.cms.api.controller.dto;

import javax.validation.constraints.NotEmpty;
import lombok.Data;

/** @author PBalarangakumar 08-02-2024 */
@Data
public class CouponMarketMappingDto {

  @NotEmpty private String couponId;

  @NotEmpty private String marketName;

  @NotEmpty private String brand;
}
