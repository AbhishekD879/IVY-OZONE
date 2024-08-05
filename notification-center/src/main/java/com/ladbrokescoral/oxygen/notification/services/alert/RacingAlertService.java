package com.ladbrokescoral.oxygen.notification.services.alert;

import com.ladbrokescoral.oxygen.notification.entities.BaseSubscription;
import com.ladbrokescoral.oxygen.notification.entities.Item;
import com.ladbrokescoral.oxygen.notification.entities.dto.RacingDTO;
import com.ladbrokescoral.oxygen.notification.utils.ObjectMapper;
import com.ladbrokescoral.oxygen.notification.utils.RedisKey;
import java.util.concurrent.TimeUnit;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.stereotype.Component;

/** Not used, Obsolete, should be deleted. */
@Component
@Qualifier("RacingAlertService")
public class RacingAlertService extends BaseAlertService {

  private RedisTemplate<String, RacingDTO> horseAlertTemplate;

  @Autowired
  public RacingAlertService(
      RedisTemplate<String, RacingDTO> horseAlertTemplate,
      @Value("${application.winalert.expiration.hours}") long timeout) {
    super(timeout);
    this.horseAlertTemplate = horseAlertTemplate;
  }

  @Override
  protected BaseSubscription saveInternal(BaseSubscription request, long timeout) {
    Item item = (Item) request;

    String key = RedisKey.forRacing(item.getEventId(), item.getPlatform());

    horseAlertTemplate
        .opsForValue()
        .set(key, ObjectMapper.toRacingDto(item), timeout, TimeUnit.HOURS);
    return item;
  }
}
