package com.coral.oxygen.middleware.ms.liveserv.impl.Validator;

import static org.junit.Assert.*;

import com.coral.oxygen.middleware.ms.liveserv.impl.incidents.IncProviderValidator;
import com.coral.oxygen.middleware.ms.liveserv.impl.incidents.IncidentsValidator;
import com.coral.oxygen.middleware.ms.liveserv.model.incidents.IncidentsEvent;
import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
import java.util.Arrays;
import java.util.List;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.junit.MockitoJUnitRunner;

@RunWith(MockitoJUnitRunner.class)
public class ValidatorTest {

  private IncidentsValidator incidentsValidator;
  private List<Integer> codes =
      Arrays.asList(
          601, 201, 202, 203, 204, 205, 206, 207, 402, 403, 208, 220, 211, 213, 219, 210, 214, 301,
          302, 401, 500, 502, 501, 215, 216, 217, 221, 218);

  @Before
  public void setUp() {
    IncProviderValidator providerValidator = new IncProviderValidator(null);
    incidentsValidator = new IncidentsValidator(codes);
  }

  @Test
  public void validVARCodeTest() {
    String data =
        "{\"incident\":{\"eventId\":\"fake593f-d146-4092-ad46-8bdf192b6ebb\",\"correlationId\":\"7645316d-ddc8-42c9-ac4e-e6668704a5f6\",\"seqId\":null,\"type\":{\"code\":601,\"description\":\"VAR\"},\"score\":null,\"periodScore\":null,\"clock\":\"46:32\",\"participant\":\"AWAY\",\"period\":\"1h\",\"timeStamp\":\"2022-01-03T12:43:40.342Z\",\"receiveTimestamp\":\"2020-07-15T23:37:07.478Z\",\"context\":{\"teamName\":\"Liverpool\",\"playerName\":\"G. Wijnaldum\",\"reasonId\":601,\"x\":\"0\",\"y\":\"0\"},\"feed\":\"OPTA\"}}";
    IncidentsEvent incidentsEvent = new IncidentsEvent("123123", data);
    boolean valid = incidentsValidator.validate(incidentsEvent);
    assertTrue(valid);
  }

  @Test
  public void incidentEventTest()
      throws NoSuchMethodException, InvocationTargetException, IllegalAccessException {
    IncidentsEvent incidentsEvent = new IncidentsEvent("123123", null);
    Method method = IncidentsEvent.class.getDeclaredMethod("getRawStructure");
    method.setAccessible(true);
    assertNull(method.invoke(incidentsEvent));
    assertNull(incidentsEvent.getIncidentsData());
  }
}
