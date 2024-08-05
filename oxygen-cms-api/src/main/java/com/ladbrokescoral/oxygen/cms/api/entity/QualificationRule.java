package com.ladbrokescoral.oxygen.cms.api.entity;

import com.ladbrokescoral.oxygen.cms.api.service.validators.Brand;
import java.util.HashMap;
import java.util.Map;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.experimental.Accessors;
import org.springframework.data.mongodb.core.mapping.Document;

@Data
@EqualsAndHashCode(callSuper = true)
@Accessors(chain = true)
@Document(collection = "qualification-rule")
public class QualificationRule extends AbstractEntity implements HasBrand {

  @Brand private String brand;

  private String message;

  private int daysToCheckActivity;

  private boolean enabled;

  private String blacklistedUsersPath;
  private Map<String, Boolean> recurringUsers = new HashMap<>();
}
