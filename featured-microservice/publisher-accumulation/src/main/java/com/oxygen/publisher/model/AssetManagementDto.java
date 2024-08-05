package com.oxygen.publisher.model;

import com.fasterxml.jackson.annotation.JsonInclude;
import java.io.Serializable;
import java.util.List;
import lombok.Data;

@JsonInclude(JsonInclude.Include.NON_NULL)
@Data
public class AssetManagementDto implements Serializable {

  private String id;
  private Integer sportId;
  private String teamName;
  private List<String> secondaryNames;
  private String primaryColour;
  private String secondaryColour;
  private boolean fiveASideToggle;
  private boolean highlightCarouselToggle;
  private Filename teamsImage;
}
