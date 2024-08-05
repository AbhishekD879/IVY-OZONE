package com.ladbrokescoral.oxygen.cms.api.entity;

import com.fasterxml.jackson.annotation.JsonAutoDetect;
import lombok.Data;
import lombok.EqualsAndHashCode;
import org.springframework.data.mongodb.core.mapping.Document;

@JsonAutoDetect(fieldVisibility = JsonAutoDetect.Visibility.ANY)
@Document(collection = SvgMigration.COLLECTION_NAME)
@Data
@EqualsAndHashCode(callSuper = true)
public class SvgMigration extends AbstractEntity implements HasBrand {

  public static final String COLLECTION_NAME = "svg-migrations";

  private String status;
  private String brand;
  private String messages;
}
