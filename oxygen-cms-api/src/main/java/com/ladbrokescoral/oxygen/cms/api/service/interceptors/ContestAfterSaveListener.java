package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.google.gson.Gson;
import com.ladbrokescoral.oxygen.cms.api.entity.Contest;
import com.ladbrokescoral.oxygen.cms.api.repository.ContestPrizeRepository;
import com.ladbrokescoral.oxygen.cms.api.service.cache.DeliveryNetworkService;
import com.ladbrokescoral.oxygen.cms.kafka.ContestPublisher;
import java.util.HashMap;
import java.util.Map;
import java.util.Optional;
import org.springframework.data.mongodb.core.mapping.event.AfterDeleteEvent;
import org.springframework.data.mongodb.core.mapping.event.AfterSaveEvent;
import org.springframework.stereotype.Component;

@Component
public class ContestAfterSaveListener extends BasicMongoEventListener<Contest> {

  private ContestPublisher contestPublisher;
  private ContestPrizeRepository contestPrizeRepository;

  public ContestAfterSaveListener(
      final DeliveryNetworkService context,
      ContestPublisher contestPublisher,
      ContestPrizeRepository contestPrizeRepository) {
    super(context);
    this.contestPublisher = contestPublisher;
    this.contestPrizeRepository = contestPrizeRepository;
  }

  /** Method that captures After save event and upload that collection to s3 bucket. */
  @Override
  public void onAfterSave(AfterSaveEvent<Contest> event) {
    /** This can be removed after contest entries story is implemented. */
    Map<String, String> headers = new HashMap<>();
    headers.put("operation", "save");
    contestPublisher.publish(null, new Gson().toJson(event.getSource()), Optional.of(headers));
  }

  @Override
  public void onAfterDelete(AfterDeleteEvent<Contest> event) {
    Map<String, String> headers = new HashMap<>();
    headers.put("operation", "delete");
    contestPrizeRepository.deleteByContestId(event.getSource().get("_id").toString());
    contestPublisher.publish(null, event.getSource().get("_id").toString(), Optional.of(headers));
  }
}
