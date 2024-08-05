package com.ladbrokescoral.oxygen.bigcompetition.dto;

import com.fasterxml.jackson.annotation.JsonInclude;
import java.util.ArrayList;
import java.util.List;
import lombok.Data;
import lombok.EqualsAndHashCode;

@Data
@EqualsAndHashCode(callSuper = true)
@JsonInclude(JsonInclude.Include.NON_EMPTY)
public class CompetitionDto extends AbstractEntity {
  private String name;
  private String uri;
  private String path;
  private Integer typeId;
  private Integer sportId;
  private Integer categoryId;
  private Integer clazzId;
  private List<CompetitionTabDto> competitionTabs = new ArrayList<>();
  private String title;
  private String background;
  private String svgBgId;
}
