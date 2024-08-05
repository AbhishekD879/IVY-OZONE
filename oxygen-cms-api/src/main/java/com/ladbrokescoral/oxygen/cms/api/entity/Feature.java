package com.ladbrokescoral.oxygen.cms.api.entity;

import com.fasterxml.jackson.annotation.JsonAutoDetect;
import com.ladbrokescoral.oxygen.cms.api.entity.menu.MediumImageAbstractMenu;
import java.time.Instant;
import java.util.List;
import javax.validation.constraints.NotBlank;
import lombok.Data;
import lombok.EqualsAndHashCode;
import org.springframework.data.mongodb.core.mapping.Document;

@JsonAutoDetect(fieldVisibility = JsonAutoDetect.Visibility.ANY)
@Document(collection = Feature.COLLECTION_NAME)
@Data
@EqualsAndHashCode(callSuper = true)
public class Feature extends SortableEntity implements HasBrand, MediumImageAbstractMenu {

  public static final String COLLECTION_NAME = "features";

  private String title_brand;
  private Integer heightMedium;
  private Integer widthMedium;
  private String uriMedium;
  private Instant validityPeriodEnd;
  private Instant validityPeriodStart;
  private String shortDescription;
  private String title;
  private List<VipLevel> vipLevels;
  private String lang;
  @NotBlank private String brand;
  @NotBlank private String showToCustomer;
  private Boolean disabled;
  private String description;
  private Filename filename;
}
