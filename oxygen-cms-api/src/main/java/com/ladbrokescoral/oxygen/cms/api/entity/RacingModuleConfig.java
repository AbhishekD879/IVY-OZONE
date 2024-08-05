package com.ladbrokescoral.oxygen.cms.api.entity;

import com.fasterxml.jackson.annotation.JsonSubTypes;
import com.fasterxml.jackson.annotation.JsonTypeInfo;
import com.ladbrokescoral.oxygen.cms.api.mapping.RacingModuleType;
import javax.validation.constraints.NotNull;
import lombok.Data;
import lombok.NoArgsConstructor;

@JsonTypeInfo(
    use = JsonTypeInfo.Id.NAME,
    property = "type",
    defaultImpl = RacingModuleConfig.class,
    visible = true)
@JsonSubTypes({
  @JsonSubTypes.Type(value = UkIrishRacingModuleConfig.class, name = "UK_AND_IRISH_RACES"),
  @JsonSubTypes.Type(value = RacingEventsModuleConfig.class, name = "INTERNATIONAL_RACES"),
  @JsonSubTypes.Type(value = RacingEventsModuleConfig.class, name = "CORAL_LEGENDS"),
  @JsonSubTypes.Type(value = RacingEventsModuleConfig.class, name = "LADBROKES_LEGENDS"),
  @JsonSubTypes.Type(
      value = VirtualRacingCarouselModuleConfig.class,
      name = "VIRTUAL_RACE_CAROUSEL"),
  @JsonSubTypes.Type(value = InternationalToteConfig.class, name = "INTERNATIONAL_TOTE_CAROUSEL")
})
@Data
@NoArgsConstructor
public class RacingModuleConfig {

  /*
  FIXME: although it's expected type to be always set, final cannot be used as it cause deserialization issues for jackson and mongo
  investigate another approaches, e.g. Builder
  */
  @NotNull private RacingModuleType type;

  public String getName() {
    return type.getTitle();
  }

  public String getAbbreviation() {
    return type.getAbbreviation();
  }
}
