package com.egalacoral.spark.timeform.model.greyhound;

import com.fasterxml.jackson.annotation.JsonIgnore;
import java.util.Set;

/**
 * Created this interface for using {@link MissingDataChecker} class for horse/grayhound
 * functionality. @TODO Align getter/setter names for horse & grayhound models
 *
 * @author Vitalij Havryk
 */
public interface TimeformEntry {

  @JsonIgnore
  public Set<Integer> getObSelectionIds();

  public String getStatusDescription();
}
