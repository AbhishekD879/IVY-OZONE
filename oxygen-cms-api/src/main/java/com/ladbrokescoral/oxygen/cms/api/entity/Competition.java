package com.ladbrokescoral.oxygen.cms.api.entity;

import com.fasterxml.jackson.annotation.JsonInclude;
import java.util.ArrayList;
import java.util.List;
import javax.validation.constraints.NotBlank;
import lombok.Data;
import lombok.EqualsAndHashCode;
import org.springframework.data.mongodb.core.mapping.DBRef;

@Data
@EqualsAndHashCode(callSuper = true)
@JsonInclude(JsonInclude.Include.NON_EMPTY)
public class Competition extends AbstractEntity {
  @NotBlank private String brand;
  @NotBlank private String name;
  @NotBlank private String uri;
  private boolean enabled;
  private String path;
  private Integer typeId;
  private Integer sportId;
  private Integer categoryId;
  private Integer clazzId;
  private String title;
  private String background;
  private String svgBgId;
  @DBRef private List<CompetitionTab> competitionTabs = new ArrayList<>();
  @DBRef private List<CompetitionParticipant> competitionParticipants = new ArrayList<>();
}
