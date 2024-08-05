package com.ladbrokescoral.oxygen.cms.api.dto;

import com.fasterxml.jackson.annotation.JsonInclude;
import com.ladbrokescoral.oxygen.cms.api.entity.Filename;
import java.util.List;
import lombok.Data;
import org.springframework.data.annotation.Id;

@JsonInclude(JsonInclude.Include.NON_NULL)
@Data
public class AssetManagementDto {

  @Id private String id;
  private Integer sportId;
  private String teamName;
  private List<String> secondaryNames;
  private String primaryColour;
  private String secondaryColour;
  private boolean fiveASideToggle;
  private boolean highlightCarouselToggle;
  private Filename teamsImage;
}
