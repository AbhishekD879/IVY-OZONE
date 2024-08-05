package com.ladbrokescoral.oxygen.cms.api.entity;

import com.ladbrokescoral.oxygen.cms.api.service.validators.Brand;
import com.ladbrokescoral.oxygen.cms.api.service.validators.DateRange;
import java.time.DayOfWeek;
import java.time.Instant;
import java.util.EnumSet;
import javax.validation.constraints.NotEmpty;
import lombok.Data;
import lombok.EqualsAndHashCode;
import org.springframework.data.mongodb.core.mapping.Document;

/**
 * JSON example: { "title": "Featured CouponSegment", Required "couponKeys": "78,26,65", Required
 * "dayOfWeek": "Tuesday", Required if `from` and `to` are not defined "from":
 * "2018-12-12T02:00:00", ISO-8601, required if `dayOfWeek` is not defined "to":
 * "2018-12-17T02:00:00" ISO-8601, required if `dayOfWeek` is not defined }
 */
@Data
@EqualsAndHashCode(callSuper = true)
@Document(collection = "coupons")
@DateRange(startDateField = "from", endDateField = "to")
public class CouponSegment extends SortableEntity implements HasBrand {

  @NotEmpty private String title;

  @NotEmpty private String couponKeys;

  private EnumSet<DayOfWeek> dayOfWeek;

  private Instant from;
  private Instant to;

  @Brand private String brand;
}
