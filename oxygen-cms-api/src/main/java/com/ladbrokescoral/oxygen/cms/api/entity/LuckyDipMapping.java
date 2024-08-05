package com.ladbrokescoral.oxygen.cms.api.entity;

import com.ladbrokescoral.oxygen.cms.api.service.validators.Brand;
import javax.validation.constraints.NotBlank;
import javax.validation.constraints.NotNull;
import lombok.Data;
import lombok.EqualsAndHashCode;
import org.springframework.data.mongodb.core.index.Indexed;
import org.springframework.data.mongodb.core.mapping.Document;

@Data
@EqualsAndHashCode(callSuper = true)
@Document(collection = "luckyDipMapping")
public class LuckyDipMapping extends SortableEntity implements HasBrand {

  @Indexed @Brand @NotBlank private String brand;

  @Indexed @NotBlank private String categoryId;

  @NotBlank private String typeIds;

  @NotNull private Boolean active;
}
