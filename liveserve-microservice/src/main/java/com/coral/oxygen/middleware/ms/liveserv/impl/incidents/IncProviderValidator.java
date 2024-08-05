package com.coral.oxygen.middleware.ms.liveserv.impl.incidents;

import com.coral.oxygen.middleware.ms.liveserv.model.incidents.IncidentsEvent;
import java.util.Arrays;
import java.util.List;
import lombok.extern.slf4j.Slf4j;

@Slf4j
public class IncProviderValidator extends Validator {

  List<String> providerData = Arrays.asList("OPTA", "AMELCO");

  public IncProviderValidator(Validator next) {
    super(next);
  }

  /**
   * This Method is used to check the OPTA ,AMELCO Feed from VAR Incidents
   *
   * @param event
   * @return true or false
   */
  @Override
  protected boolean checkCondition(IncidentsEvent event) {

    String feedValue = event.getEventStructure().getJsonString("feed").getString();

    return hasSupportedProvider(feedValue);
  }

  public boolean hasSupportedProvider(String feedValue) {
    return providerData.stream().anyMatch(v -> v.contains(feedValue.toUpperCase()));
  }
}
