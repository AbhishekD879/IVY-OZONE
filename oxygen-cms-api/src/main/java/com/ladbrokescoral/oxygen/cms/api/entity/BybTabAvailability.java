package com.ladbrokescoral.oxygen.cms.api.entity;

import com.fasterxml.jackson.annotation.JsonAutoDetect;
import javax.validation.constraints.NotBlank;
import lombok.Data;
import lombok.EqualsAndHashCode;
import org.springframework.data.mongodb.core.mapping.Document;

@JsonAutoDetect(fieldVisibility = JsonAutoDetect.Visibility.ANY)
@Document(collection = "bybTabAvailability")
@Data
@EqualsAndHashCode(callSuper = true)
public class BybTabAvailability extends AbstractEntity implements HasBrand {
  private String lang = "en";
  @NotBlank private String brand;
  private String device;
  private boolean atLeastOneBanachEventAvailable;
  private boolean displayBybTab;
}
