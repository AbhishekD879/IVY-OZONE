package com.ladbrokescoral.oxygen.bigcompetition.dto;

import com.fasterxml.jackson.annotation.JsonInclude;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.NoArgsConstructor;
import lombok.experimental.Accessors;

@Data
@EqualsAndHashCode(callSuper = true)
@JsonInclude(JsonInclude.Include.NON_EMPTY)
@NoArgsConstructor
@AllArgsConstructor
@Accessors(chain = true)
public class ParticipantDto extends AbstractEntity {
  protected String name;
  protected String obName;
  protected String abbreviation;
  protected String svgId;
  protected String isWinner;
}
