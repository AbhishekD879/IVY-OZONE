package com.ladbrokescoral.oxygen.bigcompetition.dto;

import com.fasterxml.jackson.annotation.JsonInclude;
import lombok.Builder;
import lombok.Data;
import lombok.EqualsAndHashCode;

@Data
@EqualsAndHashCode(callSuper = true)
@JsonInclude(JsonInclude.Include.NON_EMPTY)
public class ParticipantWithSvgDto extends ParticipantDto {
  private String svg;

  @Builder
  public ParticipantWithSvgDto(String name, String abbreviation, String svgId, String svg) {
    super(name, null, abbreviation, svgId, null);
    this.svg = svg;
  }
}
