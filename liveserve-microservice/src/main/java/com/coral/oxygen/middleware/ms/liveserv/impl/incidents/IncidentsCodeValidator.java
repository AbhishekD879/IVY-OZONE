package com.coral.oxygen.middleware.ms.liveserv.impl.incidents;

import com.coral.oxygen.middleware.ms.liveserv.model.incidents.IncidentsEvent;
import java.util.List;
import javax.json.JsonNumber;
import lombok.extern.slf4j.Slf4j;

@Slf4j
public class IncidentsCodeValidator extends Validator {

  private List<Integer> codes;

  public IncidentsCodeValidator(Validator next, List<Integer> codes) {
    super(next);
    this.codes = codes;
  }

  /**
   * This Method is used to check the VAR,Match Fact Codes from Incidents Objets
   *
   * @param event
   * @return true or false
   */
  @Override
  protected boolean checkCondition(IncidentsEvent event) {
    JsonNumber varCode = event.getEventStructure().getJsonObject("type").getJsonNumber("code");
    return hasSupportedVARCode(Integer.valueOf(varCode.intValue()));
  }

  /**
   * This Method is used to check only to Suppport necessary Match Fact Codes
   *
   * @param code
   * @return true or false
   */
  public boolean hasSupportedVARCode(Integer code) {
    log.info("IncidentsCodeValidator codes {}", codes);
    return codes.stream().anyMatch(c -> c.equals(code));
  }
}
