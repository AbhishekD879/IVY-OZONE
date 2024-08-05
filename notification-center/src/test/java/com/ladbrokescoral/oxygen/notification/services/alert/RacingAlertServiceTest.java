package com.ladbrokescoral.oxygen.notification.services.alert;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import com.ladbrokescoral.oxygen.notification.entities.Item;
import com.ladbrokescoral.oxygen.notification.entities.dto.RacingDTO;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.TimeUnit;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.junit.MockitoJUnitRunner;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.data.redis.core.ValueOperations;

@RunWith(MockitoJUnitRunner.class)
public class RacingAlertServiceTest {
  private static final Gson GSON = new GsonBuilder().create();
  private static final String TEST_REDIS_KEY = "horses_greyhounds:267941:ios";

  @Mock private ValueOperations<String, RacingDTO> operations;

  @Mock private RedisTemplate<String, RacingDTO> template;
  private AlertService service;
  private RacingDTO dto;

  private Item request;

  @Before
  public void setUp() {
    request = getRequestData();
    service = new RacingAlertService(template, 1);

    Mockito.when(template.opsForValue()).thenReturn(operations);

    List<String> types = new ArrayList<>();
    types.add("going_down");
    types.add("race_off");

    dto = RacingDTO.builder().eventId(267941L).platform("ios").token("hoken").types(types).build();
  }

  @Test
  public void save() {
    service.save(request);
    Mockito.verify(template.opsForValue()).set(TEST_REDIS_KEY, dto, 22L, TimeUnit.HOURS);
  }

  private Item getRequestData() {
    return GSON.fromJson(
        new InputStreamReader(
            this.getClass().getClassLoader().getResourceAsStream("requests/racing_request.json")),
        Item.class);
  }
}
