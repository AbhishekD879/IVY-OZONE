package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.entity.ContestPrize;
import com.ladbrokescoral.oxygen.cms.api.service.cache.DeliveryNetworkService;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.ContestPrizePublicService;
import java.util.List;
import java.util.Optional;
import org.springframework.data.mongodb.core.mapping.event.AfterSaveEvent;
import org.springframework.stereotype.Component;

@Component
public class ContestPrizeMapAfterSaveListener extends BasicMongoEventListener<ContestPrize> {

  private static final String PATH_TEMPLATE = "api/{0}/contest-prizes";
  private final ContestPrizePublicService service;

  public ContestPrizeMapAfterSaveListener(
      DeliveryNetworkService context, final ContestPrizePublicService service) {
    super(context);
    this.service = service;
  }

  /** Method that captures After save event and upload that collection to s3 bucket. */
  @Override
  public void onAfterSave(AfterSaveEvent<ContestPrize> event) {
    String contestId = event.getSource().getContestId();
    String brand = event.getSource().getBrand();
    List<ContestPrize> contestPrizes = service.findByContestId(contestId);
    uploadOptional(brand, PATH_TEMPLATE, contestId, Optional.of(contestPrizes));
  }
}
