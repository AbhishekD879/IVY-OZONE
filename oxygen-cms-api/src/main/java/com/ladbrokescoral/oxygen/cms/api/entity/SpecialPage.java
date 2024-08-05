package com.ladbrokescoral.oxygen.cms.api.entity;

import javax.validation.constraints.NotNull;
import lombok.Data;
import org.springframework.data.mongodb.core.mapping.Document;

@Data
@Document(collection = "specialPages")
public class SpecialPage extends AbstractEntity {
  @NotNull private String pageName;
  @NotNull private String brand;
}
