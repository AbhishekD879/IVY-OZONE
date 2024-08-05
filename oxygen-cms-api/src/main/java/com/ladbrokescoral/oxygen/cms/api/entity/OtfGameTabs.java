package com.ladbrokescoral.oxygen.cms.api.entity;

import com.ladbrokescoral.oxygen.cms.api.service.validators.Brand;
import javax.validation.constraints.NotNull;
import lombok.Data;
import lombok.EqualsAndHashCode;
import org.springframework.data.mongodb.core.mapping.Document;

@Data
@Document(collection = "otf-game-tabs")
@EqualsAndHashCode(callSuper = true)
public class OtfGameTabs extends AbstractEntity implements HasBrand {

  @Brand private String brand;

  @NotNull private String previousTabLabel;

  @NotNull private String currentTabLabel;
}
