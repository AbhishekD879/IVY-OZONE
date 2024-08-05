package com.egalacoral.spark.timeform.model.greyhound;

import com.fasterxml.jackson.annotation.JsonIgnore;
import java.util.Set;

/**
 * Created this interface for using {@link MissingDataChecker} class for horse/grayhound
 * functionality. @TODO Align getter/setter names for horse & grayhound models
 *
 * @author Vitalij Havryk
 */
public interface TimeformMeeting {

  /**
   * Gets the value of the obEventTypeId property. EntityColumn: openbet_id Summary: the unique
   * identifier for the event type Remark:
   *
   * @return set of Integer values above 0
   */
  @JsonIgnore
  Set<Integer> getMeetingObEventTypeId();

  /**
   * Gets the value of the races property. EntityColumn: race Summary: The representation of a race.
   * Remark: {@link Race }
   *
   * @return List of race entities
   */
  @JsonIgnore
  Set<? extends TimeformRace> getMeetingRaces();
}
