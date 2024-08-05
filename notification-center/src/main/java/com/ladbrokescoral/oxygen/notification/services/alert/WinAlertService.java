package com.ladbrokescoral.oxygen.notification.services.alert;

import static org.springframework.http.ResponseEntity.accepted;

import com.ladbrokescoral.oxygen.notification.entities.BaseSubscription;
import com.ladbrokescoral.oxygen.notification.entities.WinAlertSubscriptionRequest;
import com.ladbrokescoral.oxygen.notification.entities.WinalertStatus;
import com.ladbrokescoral.oxygen.notification.entities.dto.WinAlertDTO;
import com.ladbrokescoral.oxygen.notification.utils.ObjectMapper;
import com.ladbrokescoral.oxygen.notification.utils.RedisKey;
import com.newrelic.api.agent.Trace;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Optional;
import java.util.concurrent.TimeUnit;
import java.util.stream.Collectors;
import java.util.stream.Stream;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Component;
import org.springframework.util.CollectionUtils;

/** A service, used to store win-alert subscriptions to Redis. */
@Component
@Slf4j
@Qualifier("WinAlertService")
public class WinAlertService extends BaseAlertService {

  private RedisTemplate<String, WinAlertDTO> winAlertTemplate;
  private RedisTemplate<String, List<String>> winAlertSubScriptionTemplates;

  @Autowired
  public WinAlertService(
      RedisTemplate<String, WinAlertDTO> winAlertTemplate,
      @Value("${application.winalert.expiration.hours}") long timeout,
      RedisTemplate<String, List<String>> winAlertSubScriptionTemplates) {
    super(timeout);
    this.winAlertTemplate = winAlertTemplate;
    this.winAlertSubScriptionTemplates = winAlertSubScriptionTemplates;
  }

  @Override
  @Trace(dispatcher = true, metricName = "winalert/subscribe")
  protected BaseSubscription saveInternal(BaseSubscription request, long timeout) {
    WinAlertSubscriptionRequest subscription = (WinAlertSubscriptionRequest) request;
    logger.info("WinAlertSubscriptionRequest values " + subscription.toString());
    String winlAlertSubscriptionKey =
        subscription
            .getUserName()
            .concat(subscription.getToken())
            .concat(subscription.getPlatform());
    List<String> existingSub =
        winAlertSubScriptionTemplates.opsForValue().get(winlAlertSubscriptionKey);
    Optional.ofNullable(subscription.getBetIds())
        .ifPresent(
            bets ->
                bets.parallelStream()
                    .forEach(betId -> saveBetSubscriptionToRedis(subscription, betId, timeout)));
    logger.info(" WinAlertService existingSub value {}", existingSub);
    if (CollectionUtils.isEmpty(existingSub)) {
      logger.info(" WinAlertService inside the if condition");
      winAlertSubScriptionTemplates
          .opsForValue()
          .set(winlAlertSubscriptionKey, subscription.getBetIds(), timeout, TimeUnit.HOURS);
    } else {
      winAlertSubScriptionTemplates
          .opsForValue()
          .set(
              winlAlertSubscriptionKey,
              Stream.concat(
                      Optional.ofNullable(existingSub).orElseGet(Collections::emptyList).stream(),
                      subscription.getBetIds().stream())
                  .collect(Collectors.toList()),
              timeout,
              TimeUnit.HOURS);
    }

    return subscription;
  }

  public ResponseEntity<List<String>> getWinalertSubscriptionstatus(WinalertStatus request) {
    logger.info("inside getwinalaert");
    String winlAlertSubscriptionKey =
        request.getUserName().concat(request.getToken()).concat(request.getPlatform());
    List<String> betids = winAlertSubScriptionTemplates.opsForValue().get(winlAlertSubscriptionKey);
    return accepted().body(CollectionUtils.isEmpty(betids) ? Collections.emptyList() : betids);
  }

  public ResponseEntity<Boolean> deleteWinalertSubscription(WinalertStatus request) {
    String key = RedisKey.forWinAlert(request.getBetId(), request.getPlatform());
    String winlalertSubscriptionKey =
        request.getUserName().concat(request.getToken()).concat(request.getPlatform());
    List<String> existingSub =
        winAlertSubScriptionTemplates.opsForValue().get(winlalertSubscriptionKey);
    logger.info(" deleteWinalertSubscription redis key {}", key);
    boolean isdeleted = winAlertTemplate.delete(key);
    if (isdeleted && !CollectionUtils.isEmpty(existingSub)) {
      List<String> modificableList = new ArrayList<>(existingSub);
      modificableList.remove(request.getBetId());
      winAlertSubScriptionTemplates.opsForValue().set(winlalertSubscriptionKey, modificableList);
    }
    return accepted().body(isdeleted);
  }

  /**
   * Saves subscription to Redis
   *
   * @param subscriptionRequest sent from android/ios device
   * @param betId of the bet, this user made.
   * @param timeout after which, this subscription will expire
   */
  private void saveBetSubscriptionToRedis(
      WinAlertSubscriptionRequest subscriptionRequest, String betId, long timeout) {
    String key = RedisKey.forWinAlert(betId, subscriptionRequest.getPlatform());
    logger.info(" saveBetSubscriptionToRedis key {} ", key);
    winAlertTemplate
        .opsForValue()
        .set(key, ObjectMapper.toWinAlertDto(subscriptionRequest, betId), timeout, TimeUnit.HOURS);
    logger.info(" succesfully saved  BetSubscription To Redis {} ", key);
  }
}
