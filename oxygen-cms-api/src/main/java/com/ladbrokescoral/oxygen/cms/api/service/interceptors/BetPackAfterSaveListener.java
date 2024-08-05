package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.entity.BetPackEntity;
import com.ladbrokescoral.oxygen.cms.api.entity.Brand;
import com.ladbrokescoral.oxygen.cms.api.service.cache.DeliveryNetworkService;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.BetPackMarketPlacePublicService;
import java.util.List;
import java.util.stream.Collectors;
import lombok.extern.slf4j.Slf4j;
import org.apache.commons.collections4.CollectionUtils;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.data.mongodb.core.mapping.event.AfterSaveEvent;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.stereotype.Component;

@Slf4j
@Component
public class BetPackAfterSaveListener extends BasicMongoEventListener<BetPackEntity> {

  private final BetPackMarketPlacePublicService betPackMarketPlacePublicService;

  private final KafkaTemplate<String, List<String>> coralBetPackKafkaTemplate;

  @Value(value = "${coral.topic.active-bet-packs}")
  private String coralBetPackTopic;

  private static final String PATH_TEMPLATE = "api/{0}/";

  private static final String FILE_NAME = "bet-pack";

  public BetPackAfterSaveListener(
      final DeliveryNetworkService context,
      final BetPackMarketPlacePublicService betPackMarketPlacePublicService,
      KafkaTemplate<String, List<String>> coralBetPackKafkaTemplate) {
    super(context);
    this.betPackMarketPlacePublicService = betPackMarketPlacePublicService;
    this.coralBetPackKafkaTemplate = coralBetPackKafkaTemplate;
  }

  @Override
  public void onAfterSave(AfterSaveEvent<BetPackEntity> event) {
    String brand = event.getSource().getBrand();
    List<BetPackEntity> content = betPackMarketPlacePublicService.findAllBetPacksBetweenDate(brand);
    uploadCollection(brand, PATH_TEMPLATE, FILE_NAME, content);

    List<String> distinctActiveBetPackIds =
        betPackMarketPlacePublicService.getActiveBetPackByBrand(brand).stream()
            .map(BetPackEntity::getBetPackId)
            .distinct()
            .collect(Collectors.toList());
    if (CollectionUtils.isNotEmpty(distinctActiveBetPackIds) && Brand.BMA.equalsIgnoreCase(brand)) {
      coralBetPackKafkaTemplate.send(coralBetPackTopic, brand, distinctActiveBetPackIds);
      log.info(
          "coral kafka topic {} , brand {} and active bet pack Ids {}",
          coralBetPackTopic,
          brand,
          distinctActiveBetPackIds);
    }
  }
}
