package com.ladbrokescoral.oxygen.notification.services.alert;

import static com.ladbrokescoral.oxygen.notification.configs.AsyncConfig.EXECUTOR_QUALIFIER_KAFKA;

import com.ladbrokescoral.oxygen.notification.entities.Device;
import com.ladbrokescoral.oxygen.notification.entities.Payload;
import com.ladbrokescoral.oxygen.notification.entities.bet.Bet;
import com.ladbrokescoral.oxygen.notification.entities.bet.Betslip;
import com.ladbrokescoral.oxygen.notification.entities.dto.Platform;
import com.ladbrokescoral.oxygen.notification.entities.dto.WinAlertDTO;
import com.ladbrokescoral.oxygen.notification.services.SiteServerApiService;
import com.ladbrokescoral.oxygen.notification.services.notifications.NotificationsFactory;
import com.ladbrokescoral.oxygen.notification.utils.RedisKey;
import java.util.Arrays;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.stream.Collectors;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.scheduling.annotation.Async;
import org.springframework.stereotype.Service;

/**
 * Handles messages from DF kafka (betslip topic). Checks if the message is telling that the bet has
 * some winning amount, and if yes, checks if that bet is among subscribers, in that case, this
 * handler will try to send push notification via {@see NotificationsFactory.class}
 */
@Slf4j
@Service
public class WinAlertMessageHandlerImpl implements WinAlertMessageHandler {

  private static final String TYPE = "winalert";
  private static final String MESSAGE_TITLE = "You have a winner!";
  private static final String MESSAGE_FORMAT =
      "Congratulations %s, your bet on %s has won and your account has been credited with %s %.2f";
  private static final String SINGLE_EVENT_TYPE = "SGL";

  private RedisTemplate<String, WinAlertDTO> redisTemplate;
  private RedisTemplate<String, List<String>> winAlertSubScriptionTemplates;
  private NotificationsFactory notificationsFactory;

  private String winAlertDeepLink;
  private Map<String, String> betTypesMap;

  private SiteServerApiService siteServerApiService;

  @Autowired
  public WinAlertMessageHandlerImpl(
      @Value("${application.winalert.deeplink}") String winAlertDeepLink,
      RedisTemplate<String, WinAlertDTO> redisTemplate,
      NotificationsFactory notificationsFactory,
      Map<String, String> betTypesMap,
      SiteServerApiService siteServerApiService,
      RedisTemplate<String, List<String>> winAlertSubScriptionTemplates) {
    this.winAlertDeepLink = winAlertDeepLink;
    this.siteServerApiService = siteServerApiService;
    this.betTypesMap = betTypesMap;
    this.redisTemplate = redisTemplate;
    this.notificationsFactory = notificationsFactory;
    this.winAlertSubScriptionTemplates = winAlertSubScriptionTemplates;
  }

  /**
   * Fetches message from DF kafka, betslip topic.
   *
   * @param betslip that changed on OpenBet. Could be the one, that won, so it will check if it has.
   *     If bet won - will delegate this update further.
   */
  @Override
  @Async(EXECUTOR_QUALIFIER_KAFKA)
  public void handleBetslip(Betslip betslip) {
    betslip
        .getBets()
        .getBet()
        .parallelStream()
        .filter(bet -> bet.getWinningAmount() > 0)
        .forEach(this::onWin);
  }

  /**
   * Creates a parallel stream for each platform to check if there are subscribers for this bet at
   * least on one of the platforms.
   *
   * @param bet a bet that has positive winningAmount
   */
  private void onWin(Bet bet) {
    Arrays.asList(Platform.values())
        .parallelStream()
        .forEach(platform -> handlePlatform(bet, platform));
  }

  /** Checks if there are any subscribers for given bet and platform */
  private void handlePlatform(Bet bet, Platform platform) {
    String key = RedisKey.forWinAlert(bet.getBetReceipt(), platform.getName());
    logger.info("WINALERT:redis key value" + key);
    Optional.ofNullable(redisTemplate.opsForValue().get(key))
        .ifPresent(dto -> onSubscriberWin(dto, platform, key, bet));
  }

  /**
   * Called, when there is a match between won bet and subscriber. Creates payload with detailed
   * message and tries to send a notification via NotificationsFactory.java
   */
  private void onSubscriberWin(WinAlertDTO dto, Platform platform, String key, Bet bet) {

    logger.info(
        "WINALERT: Trying to send notification - bet won for subscriber: " + dto.toString());
    Device device = new Device(dto.getToken(), platform, dto.getAppVersionInt());
    String winlAlertSubscriptionKey =
        dto.getUserName().concat(dto.getToken()).concat(dto.getPlatform());
    List<String> existingSub =
        winAlertSubScriptionTemplates.opsForValue().get(winlAlertSubscriptionKey);
    Payload payload =
        Payload.builder()
            .message(MESSAGE_TITLE)
            .status(getMessage(dto, bet))
            .type(TYPE)
            .deepLink(winAlertDeepLink)
            .build();

    if (notificationsFactory.notify(device, payload)) {
      logger.info(
          "WINALERT: Removing subscription. Notification successfully sent to subscriber: "
              + dto.toString());
      redisTemplate.delete(key);
      if (existingSub != null) {
        List<String> sub =
            existingSub.stream()
                .filter(subs -> !subs.equals(dto.getBetId()))
                .collect(Collectors.toList());
        winAlertSubScriptionTemplates.opsForValue().set(winlAlertSubscriptionKey, sub);
      }

    } else {
      logger.warn("WINALERT: Could not send notification to subscriber: " + dto.toString());
    }
  }

  /** Composes a message for push notification. */
  private String getMessage(WinAlertDTO dto, Bet bet) {
    return String.format(
        MESSAGE_FORMAT,
        dto.getUserName(),
        getBetDescription(bet),
        bet.getCurrencyCode(),
        bet.getWinningAmount());
  }

  /**
   * Calls SiteServer to get the info about selection if the type of bet is 'single' Otherwise it
   * will just return the bet type
   */
  private String getBetDescription(Bet bet) {
    if (bet.getBetType().equals(SINGLE_EVENT_TYPE)) {
      // if bet type is single then it has only one leg with one part, so it's safe to
      String selectionId = bet.getLegs().get(0).getParts().get(0).getSelectionKey();
      return siteServerApiService.getOutcomeName(selectionId);
    } else {
      return betTypesMap.get(bet.getBetType());
    }
  }
}
