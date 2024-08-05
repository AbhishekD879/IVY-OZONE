package com.ladbrokescoral.oxygen.cms.api.entity.questionengine;

import com.ladbrokescoral.oxygen.cms.api.entity.AbstractEntity;
import com.ladbrokescoral.oxygen.cms.api.entity.HasBrand;
import com.ladbrokescoral.oxygen.cms.api.service.validators.Brand;
import javax.validation.constraints.NotBlank;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.experimental.Accessors;
import org.hibernate.validator.constraints.Range;
import org.springframework.data.mongodb.core.mapping.Document;
import org.springframework.validation.annotation.Validated;

@Validated
@Data
@Accessors(chain = true)
@EqualsAndHashCode(callSuper = true)
@Document(collection = "rss-reward")
public class RssReward extends AbstractEntity implements HasBrand {
  @Range(max = 500, message = "coin should be max of 500")
  private Integer coins;

  private String sitecoreTemplateId;
  private String source;
  @NotBlank private String subSource;
  @NotBlank private String product;
  private boolean enabled;
  @Brand private String brand;
}
