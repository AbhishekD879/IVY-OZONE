package com.coral.oxygen.middleware.ms.liveserv.impl.incidents;

import com.coral.oxygen.middleware.ms.liveserv.model.incidents.IncidentsEvent;
import java.util.List;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

@Slf4j
@Service
public class IncidentsValidator {

  private Validator validator;

  public IncidentsValidator(@Value("${incident.sport.codes}") List<Integer> codes) {
    IncProviderValidator providerValidator = new IncProviderValidator(null);
    this.validator = new IncidentsCodeValidator(providerValidator, codes);
  }

  /**
   * This Method is used to validate the VAR & Match Facts Messages
   *
   * @param incidentsEvent
   * @return true or false
   */
  public boolean validate(IncidentsEvent incidentsEvent) {
    return validator.validate(incidentsEvent);
  }
}
