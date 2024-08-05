package com.coral.oxygen.middleware.ms.liveserv.impl.Validator;

import static org.junit.Assert.*;

import com.coral.oxygen.middleware.ms.liveserv.impl.incidents.IncProviderValidator;
import com.coral.oxygen.middleware.ms.liveserv.impl.incidents.IncidentsCodeValidator;
import com.coral.oxygen.middleware.ms.liveserv.impl.incidents.Validator;
import com.coral.oxygen.middleware.ms.liveserv.model.incidents.IncidentsEvent;
import java.util.Arrays;
import java.util.List;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.junit.MockitoJUnitRunner;

@RunWith(MockitoJUnitRunner.class)
public class IncidentValidatorTest {

  private Validator incidentValidator;

  private List<Integer> codes =
      Arrays.asList(
          601, 201, 202, 203, 204, 205, 206, 207, 402, 403, 208, 220, 211, 213, 219, 210, 214, 301,
          302, 401, 500, 502, 501, 215, 216, 217, 221, 218);

  @Before
  public void setUp() {
    IncProviderValidator providerValidator = new IncProviderValidator(null);
    this.incidentValidator = new IncidentsCodeValidator(providerValidator, codes);
  }

  @Test
  public void validVARCodeTest() {
    String data =
        "{\"incident\":{\"eventId\":\"fake11a5-53bb-42ad-8f4c-7a8fa40ab9fa\",\"correlationId\":\"04ed57c3-ac16-49c2-bd50-960a570240fe\",\"seqId\":null,\"type\":{\"code\":601,\"description\":\"VAR\"},\"score\":null,\"periodScore\":null,\"clock\":\"46:32\",\"participant\":\"AWAY\",\"period\":\"1h\",\"timeStamp\":\"2021-12-30T12:30:26.527Z\",\"receiveTimestamp\":\"2020-07-15T23:37:07.478Z\",\"context\":{\"teamName\":\"Liverpool\",\"playerName\":\"G. Wijnaldum\",\"reasonId\":601,\"x\":\"0\",\"y\":\"0\"},\"feed\":\"OPTA\"}}";
    IncidentsEvent incidentsEvent = new IncidentsEvent("123123", data);
    boolean valid = incidentValidator.validate(incidentsEvent);
    assertTrue(valid);
  }

  @Test
  public void incidentValidTest() {
    String data =
        "{\"incident\":{\"eventId\":\"fake11a5-53bb-42ad-8f4c-7a8fa40ab9fa\",\"correlationId\":\"04ed57c3-ac16-49c2-bd50-960a570240fe\",\"seqId\":null,\"type\":{\"code\":601,\"description\":\"VAR\"},\"score\":null,\"periodScore\":null,\"clock\":\"46:32\",\"participant\":\"AWAY\",\"period\":\"1h\",\"timeStamp\":\"2021-12-30T12:30:26.527Z\",\"receiveTimestamp\":\"2020-07-15T23:37:07.478Z\",\"context\":{\"teamName\":\"Liverpool\",\"playerName\":\"G. Wijnaldum\",\"reasonId\":601,\"x\":\"0\",\"y\":\"0\"},\"feed\":\"OPTA\"}}";
    IncidentsEvent incidentsEvent = new IncidentsEvent("123123", data);
    boolean valid = incidentValidator.validate(incidentsEvent);
    assertTrue(valid);
  }

  @Test
  public void invalidIncidentKeyTest() {
    String data =
        "{\"incidentTest\":{\"eventId\":\"fake11a5-53bb-42ad-8f4c-7a8fa40ab9fa\",\"correlationId\":\"04ed57c3-ac16-49c2-bd50-960a570240fe\",\"seqId\":null,\"type\":{\"code\":112,\"description\":\"VAR\"},\"score\":null,\"periodScore\":null,\"clock\":\"46:32\",\"participant\":\"AWAY\",\"period\":\"1h\",\"timeStamp\":\"2021-12-30T12:30:26.527Z\",\"receiveTimestamp\":\"2020-07-15T23:37:07.478Z\",\"context\":{\"teamName\":\"Liverpool\",\"playerName\":\"G. Wijnaldum\",\"reasonId\":601,\"x\":\"0\",\"y\":\"0\"},\"feed\":\"OPTA\"}}";
    IncidentsEvent incidentsEvent = new IncidentsEvent("123123", data);
    boolean valid = incidentValidator.validate(incidentsEvent);
    assertFalse(valid);
  }

  @Test
  public void invalidVARCodeTestForIncidents() {
    String data =
        "{\"incident\":{\"eventId\":\"fake11a5-53bb-42ad-8f4c-7a8fa40ab9fa\",\"correlationId\":\"04ed57c3-ac16-49c2-bd50-960a570240fe\",\"seqId\":234,\"type\":{\"code\":112,\"description\":\"VAR\"},\"score\":null,\"periodScore\":null,\"clock\":\"46:32\",\"participant\":\"AWAY\",\"period\":\"1h\",\"timeStamp\":\"2021-12-30T12:30:26.527Z\",\"receiveTimestamp\":\"2020-07-15T23:37:07.478Z\",\"context\":{\"teamName\":\"Liverpool\",\"playerName\":\"G. Wijnaldum\",\"reasonId\":601,\"x\":\"0\",\"y\":\"0\"},\"feed\":\"OPTA\"}}";
    IncidentsEvent incidentsEvent = new IncidentsEvent("123123", data);
    boolean valid = incidentValidator.validate(incidentsEvent);
    assertFalse(valid);
  }

  @Test
  public void invalidIncidentProviderTest() {
    String data =
        "{\"incident\":{\"eventId\":\"fake11a5-53bb-42ad-8f4c-7a8fa40ab9fa\",\"correlationId\":\"04ed57c3-ac16-49c2-bd50-960a570240fe\",\"seqId\":235,\"type\":{\"code\":601,\"description\":\"VAR\"},\"score\":null,\"periodScore\":null,\"clock\":\"46:32\",\"participant\":\"AWAY\",\"period\":\"1h\",\"timeStamp\":\"2021-12-30T12:30:26.527Z\",\"receiveTimestamp\":\"2020-07-15T23:37:07.478Z\",\"context\":{\"teamName\":\"Liverpool\",\"playerName\":\"G. Wijnaldum\",\"reasonId\":601,\"x\":\"0\",\"y\":\"0\"},\"feed\":\"BWIN\"}}";
    IncidentsEvent incidentsEvent = new IncidentsEvent("123123", data);
    IncProviderValidator providerValidator = new IncProviderValidator(null);
    boolean valid = providerValidator.validate(incidentsEvent);
    assertFalse(valid);
  }
}
