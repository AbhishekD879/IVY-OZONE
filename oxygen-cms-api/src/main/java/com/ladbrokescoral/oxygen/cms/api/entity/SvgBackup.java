package com.ladbrokescoral.oxygen.cms.api.entity;

import com.fasterxml.jackson.annotation.JsonAutoDetect;
import lombok.Data;
import lombok.EqualsAndHashCode;
import org.springframework.data.mongodb.core.mapping.Document;

@JsonAutoDetect(fieldVisibility = JsonAutoDetect.Visibility.ANY)
@Document(collection = SvgBackup.COLLECTION_NAME)
@Data
@EqualsAndHashCode(callSuper = true)
public class SvgBackup extends AbstractEntity implements HasBrand {
  public static final String COLLECTION_NAME = "svg-backups";

  private String collectionName;
  private String collectionId;
  private String svgId;
  private String svg;
  private String brand;
}
