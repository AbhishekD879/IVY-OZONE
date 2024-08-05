package com.ladbrokescoral.oxygen.cms.api.entity;

import com.fasterxml.jackson.annotation.JsonAutoDetect;
import com.ladbrokescoral.oxygen.cms.api.service.validators.Brand;
import javax.validation.constraints.NotBlank;
import javax.validation.constraints.NotNull;
import lombok.Data;
import lombok.EqualsAndHashCode;
import org.springframework.data.mongodb.core.mapping.Document;

@JsonAutoDetect(fieldVisibility = JsonAutoDetect.Visibility.ANY)
@Document(collection = "badge")
@Data
@EqualsAndHashCode(callSuper = true)
public class Badge extends AbstractEntity implements HasBrand {

  @Brand private String brand;

  @NotBlank private String label;

  @NotBlank private String rulesDisplay;

  private boolean lastUpdatedFlag;

  @NotBlank private String viewButtonLabel;

  private boolean viewButton;

  @NotNull private String lbrRedirectionUrl;

  @NotNull private String lbrRedirectionLabel;

  private boolean viewLbrUrl;

  private boolean viewBadges;
}
