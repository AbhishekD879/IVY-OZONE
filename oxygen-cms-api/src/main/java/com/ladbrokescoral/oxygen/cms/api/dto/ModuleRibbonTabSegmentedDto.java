package com.ladbrokescoral.oxygen.cms.api.dto;

import com.ladbrokescoral.oxygen.cms.api.entity.OSDevice;
import java.time.Instant;
import lombok.Data;
import lombok.EqualsAndHashCode;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Field;

@Data
@EqualsAndHashCode(callSuper = true)
public class ModuleRibbonTabSegmentedDto extends AbstractSegmentDto {
  @Id private String id;
  private String brand;
  private String directiveName;
  private String key;
  private String lang = "en";
  private String targetUri;
  private String title;
  private String title_brand;
  private Boolean visible = true;
  private String showTabOn;

  @Field("ID")
  private String internalId;

  private OSDevice devices = new OSDevice(true, true, true);
  private String url;
  private Integer hubIndex;
  private Instant displayFrom;
  private Instant displayTo;
}
