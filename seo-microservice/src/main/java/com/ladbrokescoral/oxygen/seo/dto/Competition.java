package com.ladbrokescoral.oxygen.seo.dto;

import com.fasterxml.jackson.annotation.JsonInclude;
import java.io.Serializable;
import java.util.ArrayList;
import java.util.List;
import lombok.Data;

@Data
@JsonInclude(JsonInclude.Include.NON_EMPTY)
public class Competition implements Serializable {
  private String brand;
  private String name;
  private String uri;
  private boolean enabled;
  private String path;
  private Integer typeId;
  private Integer sportId;
  private Integer categoryId;
  private Integer clazzId;
  private String title;
  private String background;
  private String svgBgId;
  private List<CompetitionTab> competitionTabs = new ArrayList<>();
}
