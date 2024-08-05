package com.ladbrokescoral.oxygen.notification.services.alert;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import com.ladbrokescoral.oxygen.notification.entities.WinAlertSubscriptionRequest;
import com.ladbrokescoral.oxygen.notification.entities.WinalertStatus;
import com.ladbrokescoral.oxygen.notification.entities.dto.WinAlertDTO;
import java.io.InputStreamReader;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import java.util.concurrent.TimeUnit;
import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.junit.MockitoJUnitRunner;
import org.mockito.junit.jupiter.MockitoSettings;
import org.mockito.quality.Strictness;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.data.redis.core.ValueOperations;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;

@RunWith(MockitoJUnitRunner.class)
@MockitoSettings(strictness = Strictness.LENIENT)
public class WinAlertServiceTest {

  private static final Gson GSON = new GsonBuilder().create();

  private static final String TEST_BET_ID_ONE = "O/0229180/0000027";
  private static final String TEST_BET_ID_TWO = "O/0229180/0000028";
  private static final String TEST_BET_ID_THREE = "O/0229180/0000029";

  private static final String TEST_REDIS_KEY_ONE = "win_alert:" + TEST_BET_ID_ONE + ":helium_ios";
  private static final String TEST_REDIS_KEY_TWO = "win_alert:" + TEST_BET_ID_TWO + ":helium_ios";
  private static final String TEST_REDIS_KEY_THREE =
      "win_alert:" + TEST_BET_ID_THREE + ":helium_ios";

  @Mock private ValueOperations<String, WinAlertDTO> operations;

  @Mock private RedisTemplate<String, WinAlertDTO> template;

  @Mock RedisTemplate<String, List<String>> winAlertSubScriptionTemplates;

  @Mock private ValueOperations<String, List<String>> winAlertOperations;
  private WinAlertService service;
  String WinlalertSubscriptionKey =
      "Johnny English" + "jdsBKBNr433JSDIfsdjhfs4f3U932di2" + "helium_ios";

  private WinAlertDTO dtoOne;
  private WinAlertDTO dtoTwo;
  private WinAlertDTO dtoThree;

  private WinAlertSubscriptionRequest request;

  @Before
  public void setUp() {
    request = getRequestData();
    service = new WinAlertService(template, 1, winAlertSubScriptionTemplates);

    Mockito.when(template.opsForValue()).thenReturn(operations);
    Mockito.when(winAlertSubScriptionTemplates.opsForValue()).thenReturn(winAlertOperations);
    dtoOne = getDtoForBetId(TEST_BET_ID_ONE);
    dtoTwo = getDtoForBetId(TEST_BET_ID_TWO);
    dtoThree = getDtoForBetId(TEST_BET_ID_THREE);
  }

  private WinAlertDTO getDtoForBetId(String betId) {
    return WinAlertDTO.builder()
        .betId(betId)
        .platform("helium_ios")
        .token("jdsBKBNr433JSDIfsdjhfs4f3U932di2")
        .userName("Johnny English")
        .build();
  }

  @Test
  public void shouldSave() {
    service.save(request);

    verifyDTOSaved(TEST_REDIS_KEY_ONE, dtoOne);
    verifyDTOSaved(TEST_REDIS_KEY_TWO, dtoTwo);
    verifyDTOSaved(TEST_REDIS_KEY_THREE, dtoThree);
  }

  @Test
  public void shouldSaves() {
    Mockito.when(winAlertOperations.get(WinlalertSubscriptionKey))
        .thenReturn(Arrays.asList("O/0229180/0000027"));
    service.save(request);
    verifyDTO(
        WinlalertSubscriptionKey,
        Arrays.asList(
            "O/0229180/0000027", "O/0229180/0000027", "O/0229180/0000028", "O/0229180/0000029"));
  }

  private void verifyDTOSaved(String key, WinAlertDTO dto) {
    Mockito.verify(template.opsForValue()).set(key, dto, 22L, TimeUnit.HOURS);
  }

  private void verifyDTO(String key, List<String> betIds) {
    Mockito.verify(winAlertSubScriptionTemplates.opsForValue())
        .set(key, betIds, 22L, TimeUnit.HOURS);
  }

  private WinAlertSubscriptionRequest getRequestData() {
    return GSON.fromJson(
        new InputStreamReader(
            this.getClass().getClassLoader().getResourceAsStream("requests/winalert_request.json")),
        WinAlertSubscriptionRequest.class);
  }

  @Test
  public void getWinalerSub() {
    Mockito.when(winAlertSubScriptionTemplates.opsForValue()).thenReturn(winAlertOperations);
    Mockito.when(winAlertOperations.get("testtesttest"))
        .thenReturn(Arrays.asList("O/0229182/0000028"));
    ResponseEntity responseEntity =
        service.getWinalertSubscriptionstatus(new WinalertStatus("test", "test", "test", "test"));
    Assert.assertNotNull(responseEntity);
    Assert.assertEquals(HttpStatus.ACCEPTED, responseEntity.getStatusCode());
  }

  @Test
  public void getWinalerNegativeSub() {
    ResponseEntity responseEntity =
        service.getWinalertSubscriptionstatus(new WinalertStatus("test", "test", "test", "test"));
    Assert.assertNotNull(responseEntity);
    Assert.assertEquals(HttpStatus.ACCEPTED, responseEntity.getStatusCode());
  }

  @Test
  public void deleteWinalerSub() {
    ResponseEntity responseEntity =
        service.deleteWinalertSubscription(new WinalertStatus("test", "test", "test", "test"));
    Assert.assertNotNull(responseEntity);
    Assert.assertEquals(HttpStatus.ACCEPTED, responseEntity.getStatusCode());
  }

  @Test
  public void deleteWinalerSubforvalues() {
    service.save(request);
    verifyDTOSaved(TEST_REDIS_KEY_ONE, dtoOne);
    Mockito.when(winAlertOperations.get(WinlalertSubscriptionKey))
        .thenReturn(Arrays.asList("O/0229180/0000027"));
    Mockito.when(template.delete("win_alert:O/0229180/0000027:helium_ios"))
        .thenReturn(Boolean.TRUE);
    ResponseEntity responseEntity =
        service.deleteWinalertSubscription(
            new WinalertStatus(
                "Johnny English",
                "jdsBKBNr433JSDIfsdjhfs4f3U932di2",
                "helium_ios",
                "O/0229180/0000027"));

    Assert.assertNotNull(responseEntity);
    Assert.assertEquals(HttpStatus.ACCEPTED, responseEntity.getStatusCode());
  }

  @Test
  public void deleteWinalernullSubforvaluesempty() {
    service.save(request);
    verifyDTOSaved(TEST_REDIS_KEY_ONE, dtoOne);
    Mockito.when(winAlertOperations.get(WinlalertSubscriptionKey))
        .thenReturn(Collections.emptyList());
    Mockito.when(template.delete("win_alert:O/0229180/0000027:helium_ios"))
        .thenReturn(Boolean.TRUE);
    ResponseEntity responseEntity =
        service.deleteWinalertSubscription(
            new WinalertStatus(
                "Johnny English",
                "jdsBKBNr433JSDIfsdjhfs4f3U932di2",
                "helium_ios",
                "O/0229180/0000027"));

    Assert.assertNotNull(responseEntity);
    Assert.assertEquals(HttpStatus.ACCEPTED, responseEntity.getStatusCode());
  }

  @Test
  public void deleteWinalerSubwithoutvalues() {
    service.save(request);
    verifyDTOSaved(TEST_REDIS_KEY_ONE, dtoOne);
    Mockito.when(winAlertOperations.get(WinlalertSubscriptionKey))
        .thenReturn(Arrays.asList("O/0229180/0000027"));
    Mockito.when(template.delete("win_alert:O/0229180/0000027:helium_ios"))
        .thenReturn(Boolean.FALSE);
    ResponseEntity responseEntity =
        service.deleteWinalertSubscription(
            new WinalertStatus(
                "Johnny English",
                "jdsBKBNr433JSDIfsdjhfs4f3U932di2",
                "helium_ios",
                "O/0229180/0000027"));

    Assert.assertNotNull(responseEntity);
    Assert.assertEquals(HttpStatus.ACCEPTED, responseEntity.getStatusCode());
  }

  @Test
  public void deleteWinalerSubwithoutSubvalues() {
    service.save(request);
    verifyDTOSaved(TEST_REDIS_KEY_ONE, dtoOne);
    Mockito.when(winAlertOperations.get(WinlalertSubscriptionKey))
        .thenReturn(Collections.emptyList());
    Mockito.when(template.delete("win_alert:O/0229180/0000027:helium_ios"))
        .thenReturn(Boolean.FALSE);
    ResponseEntity responseEntity =
        service.deleteWinalertSubscription(
            new WinalertStatus(
                "Johnny English",
                "jdsBKBNr433JSDIfsdjhfs4f3U932di2",
                "helium_ios",
                "O/0229180/0000027"));

    Assert.assertNotNull(responseEntity);
    Assert.assertEquals(HttpStatus.ACCEPTED, responseEntity.getStatusCode());
  }

  @Test
  public void deleteWinalerSubnullSubvalues() {
    service.save(request);
    verifyDTOSaved(TEST_REDIS_KEY_ONE, dtoOne);
    Mockito.when(winAlertOperations.get(WinlalertSubscriptionKey)).thenReturn(null);
    Mockito.when(template.delete("win_alert:O/0229180/0000027:helium_ios"))
        .thenReturn(Boolean.FALSE);
    ResponseEntity responseEntity =
        service.deleteWinalertSubscription(
            new WinalertStatus(
                "Johnny English",
                "jdsBKBNr433JSDIfsdjhfs4f3U932di2",
                "helium_ios",
                "O/0229180/0000027"));

    Assert.assertNotNull(responseEntity);
    Assert.assertEquals(HttpStatus.ACCEPTED, responseEntity.getStatusCode());
  }
}
