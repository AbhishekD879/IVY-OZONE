package com.coral.oxygen.middleware.featured.consumer.sportpage;

import com.google.common.collect.Sets;
import java.util.Arrays;
import java.util.Optional;
import java.util.Set;
import java.util.stream.Stream;
import lombok.AccessLevel;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.RequiredArgsConstructor;
import org.apache.commons.lang3.StringUtils;

@Getter
@RequiredArgsConstructor(access = AccessLevel.PRIVATE)
@AllArgsConstructor(access = AccessLevel.PRIVATE)
public enum RacingModuleType {
  /**
   * order of types is important for logic to be consistent with UI as here we duplicate UI logic
   * implemented on EDP as well
   */
  UK_AND_IRISH_RACES("UIR", true, "UK,IE", "SP"),
  INTERNATIONAL_RACES("IR", true, "FR,AE,ZA,IN,US,AU,CL,INT", "SP"),
  LEGENDS_VIRTUAL_RACES("LVR", true, "VR", "SP"),
  INTERNATIONAL_TOTE_CAROUSEL("ITC"),
  VIRTUAL_RACE_CAROUSEL("VRC"),
  OTHER("");

  private final String abbreviation;
  private boolean isEventsModule;
  private String typeFlags;
  private String excludeTypeFlags;

  private boolean intersectsTypeFlags(Set<String> flags) {
    if (StringUtils.isEmpty(getTypeFlags())) {
      return false;
    }
    return Stream.of(typeFlags.split(",")).anyMatch(flags::contains);
  }

  public static RacingModuleType from(String abbreviation) {
    return Arrays.stream(values())
        .filter(t -> t.getAbbreviation().equalsIgnoreCase(abbreviation))
        .findAny()
        .orElse(OTHER);
  }

  /**
   * Implementation corresponds to UI logic On UI (racing and edp) they traverse flags in order:
   * ['UK', 'IE', 'FR', 'AE', 'ZA', 'IN', 'US', 'AU', 'CL', 'INT', 'VR'] and define type by first
   * match,
   *
   * @param flags - event typeFlags
   * @return first racing type matching event typeFlags, INTERNATIONAL_RACES by default
   */
  public static RacingModuleType getTypeByFlags(String flags) {
    Set<String> searchedFlags =
        Sets.newHashSet(Optional.ofNullable(flags).map(f -> f.split(",")).orElse(new String[0]));
    return Arrays.stream(values())
        .filter(t -> t.intersectsTypeFlags(searchedFlags))
        .findAny()
        .orElse(INTERNATIONAL_RACES);
  }
}
