package com.egalacoral.spark.timeform.model.greyhound;

import com.fasterxml.jackson.annotation.JsonIgnore;
import java.util.Set;

/**
 * Created this interface for using {@link MissingDataChecker} class for horse/grayhound
 * functionality. @TODO Align getter/setter names for horse & grayhound models
 *
 * @author Vitalij Havryk
 */
public interface TimeformRace {

  @JsonIgnore
  public Set<Integer> getRaceObEventIds();

  @JsonIgnore
  public Set<? extends TimeformEntry> getRaceEntries();
}
