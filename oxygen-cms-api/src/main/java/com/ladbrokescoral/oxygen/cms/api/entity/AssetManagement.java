package com.ladbrokescoral.oxygen.cms.api.entity;

import com.fasterxml.jackson.annotation.JsonInclude;
import com.ladbrokescoral.oxygen.cms.api.service.validators.Brand;
import java.util.List;
import lombok.Data;
import lombok.EqualsAndHashCode;
import org.springframework.data.mongodb.core.index.Indexed;
import org.springframework.data.mongodb.core.mapping.Document;

@Data
@EqualsAndHashCode(callSuper = true)
@Document(collection = "assetmanagement")
@JsonInclude(JsonInclude.Include.NON_NULL)
public class AssetManagement extends AbstractEntity implements HasBrand {

  private Integer sportId;

  @Indexed private String teamName;

  private List<String> secondaryNames;

  private String primaryColour;

  private String secondaryColour;

  @Brand private String brand;

  private boolean fiveASideToggle;

  private boolean highlightCarouselToggle;

  private Filename teamsImage;

  private boolean active;
}
