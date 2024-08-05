package com.egalacoral.spark.timeform.model;

import com.egalacoral.spark.siteserver.model.Type;
import java.util.Collections;
import java.util.Date;
import java.util.List;

public class MissingTimeFormData {

  private final Date date;
  private final List<Type> lostTypes;
  private final List<LostEvent> lostEvents;
  private final List<LostOutcome> lostOutcomes;

  public MissingTimeFormData(
      Date date, List<Type> lostTypes, List<LostEvent> lostEvents, List<LostOutcome> lostOutcomes) {
    this.date = date;
    this.lostTypes = lostTypes;
    this.lostEvents = lostEvents;
    this.lostOutcomes = lostOutcomes;
  }

  public Date getDate() {
    return date;
  }

  public List<Type> getLostTypes() {
    return Collections.unmodifiableList(lostTypes);
  }

  public List<LostEvent> getLostEvents() {
    return Collections.unmodifiableList(lostEvents);
  }

  public List<LostOutcome> getLostOutcomes() {
    return Collections.unmodifiableList(lostOutcomes);
  }
}
