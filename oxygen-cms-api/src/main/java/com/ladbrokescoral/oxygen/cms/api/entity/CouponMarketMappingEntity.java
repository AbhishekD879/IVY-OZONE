package com.ladbrokescoral.oxygen.cms.api.entity;

import com.ladbrokescoral.oxygen.cms.api.service.validators.Brand;
import javax.validation.constraints.NotEmpty;
import lombok.Data;
import lombok.EqualsAndHashCode;
import org.springframework.data.mongodb.core.mapping.Document;

/** @author PBalarangakumar 08-02-2024 */
@Data
@EqualsAndHashCode(callSuper = true)
@Document(collection = "coupon-market-mapping")
public class CouponMarketMappingEntity extends SortableEntity implements HasBrand {

  @NotEmpty private String couponId;

  @NotEmpty private String marketName;

  @Brand private String brand;
}
