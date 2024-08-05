package com.ladbrokescoral.oxygen.cms.api.entity;

import com.fasterxml.jackson.annotation.JsonAutoDetect;
import com.ladbrokescoral.oxygen.cms.api.entity.segment.AbstractSegmentEntity;
import com.ladbrokescoral.oxygen.cms.api.entity.segment.SegmentEntity;
import com.ladbrokescoral.oxygen.cms.api.service.validators.DateRange;
import java.time.Instant;
import javax.validation.constraints.NotBlank;
import javax.validation.constraints.NotNull;
import lombok.Data;
import lombok.EqualsAndHashCode;
import org.springframework.data.mongodb.core.mapping.Document;
import org.springframework.data.mongodb.core.mapping.Field;

@JsonAutoDetect(fieldVisibility = JsonAutoDetect.Visibility.ANY)
@Document(collection = "moduleribbontabs")
@Data
@EqualsAndHashCode(callSuper = true)
@DateRange(startDateField = "displayFrom", endDateField = "displayTo")
public class ModuleRibbonTab extends AbstractSegmentEntity implements HasBrand, SegmentEntity {

  @NotBlank private String brand;
  @NotBlank private String directiveName;
  private String key;
  private String lang = "en";
  private String targetUri;
  @NotNull @NotBlank private String title;
  private String title_brand;
  private Boolean visible = true;
  @NotBlank private String showTabOn;

  @NotBlank
  @Field("ID")
  private String internalId;

  private OSDevice devices = new OSDevice(true, true, true);
  @NotBlank private String url;
  private Integer hubIndex;
  private Instant displayFrom;
  private Instant displayTo;
  private Boolean bybVisble;
}
