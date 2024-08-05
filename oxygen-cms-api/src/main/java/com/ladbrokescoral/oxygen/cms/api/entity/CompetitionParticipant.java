package com.ladbrokescoral.oxygen.cms.api.entity;

import javax.validation.constraints.NotBlank;
import lombok.Data;
import lombok.EqualsAndHashCode;

@Data
@EqualsAndHashCode(callSuper = true)
public class CompetitionParticipant extends AbstractEntity {

  @NotBlank private String obName;
  private String fullName;
  private String abbreviation;
  private String svg;
  private String svgId;
  private String svgFilename;

  public static CompetitionParticipant setSvgFields(
      CompetitionParticipant entity, String svg, String id, String svgFilename) {
    entity.setSvgFilename(svgFilename);
    entity.setSvg(svg);
    entity.setSvgId(id);
    return entity;
  }
}
