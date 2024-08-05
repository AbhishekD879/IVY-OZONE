package com.ladbrokescoral.oxygen.cms.api.entity;

import com.ladbrokescoral.oxygen.cms.api.service.validators.Brand;
import java.util.List;
import javax.validation.Valid;
import javax.validation.constraints.NotEmpty;
import lombok.Data;
import lombok.EqualsAndHashCode;
import org.springframework.data.mongodb.core.mapping.Document;

/**
 * JSON example: { "title": "Match Result", Required "templateMarketName": "Match Betting", Required
 * "header": ['Home','Draw','Away'], Required }
 */
@Data
@EqualsAndHashCode(callSuper = true)
@Document(collection = "couponmarketselectors")
public class CouponMarketSelector extends SortableEntity implements HasBrand {

  @NotEmpty private String title;

  @NotEmpty private String templateMarketName;

  @Valid private List<@NotEmpty String> header;

  @Brand private String brand;
}
