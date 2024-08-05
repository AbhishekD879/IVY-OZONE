package com.ladbrokescoral.oxygen.cms.api.entity;

import com.ladbrokescoral.oxygen.cms.api.service.validators.Brand;
import javax.validation.constraints.NotEmpty;
import lombok.Data;
import lombok.EqualsAndHashCode;
import org.springframework.data.mongodb.core.mapping.Document;

@Data
@EqualsAndHashCode(callSuper = true)
@Document(collection = "fiveasideformation")
public class FiveASideFormation extends SortableEntity implements HasBrand {
  @NotEmpty private String title;
  @NotEmpty private String actualFormation;
  private String position1;
  private BanachMarket stat1;
  private String position2;
  private BanachMarket stat2;
  private String position3;
  private BanachMarket stat3;
  private String position4;
  private BanachMarket stat4;
  private String position5;
  private BanachMarket stat5;
  @Brand private String brand;
}
