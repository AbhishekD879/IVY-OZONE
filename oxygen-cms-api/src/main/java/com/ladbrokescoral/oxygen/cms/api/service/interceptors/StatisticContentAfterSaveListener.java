package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.controller.dto.StatisticContent;
import com.ladbrokescoral.oxygen.cms.api.dto.StatisticContentDto;
import com.ladbrokescoral.oxygen.cms.api.service.cache.DeliveryNetworkService;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.StatisticContentPublicService;
import java.util.List;
import org.bson.Document;
import org.springframework.data.mongodb.core.mapping.event.AfterDeleteEvent;
import org.springframework.data.mongodb.core.mapping.event.AfterSaveEvent;
import org.springframework.stereotype.Component;
import org.springframework.util.Assert;

/**
 * Class that listens {@link com.ladbrokescoral.oxygen.cms.api.controller.dto.StatisticContent} s
 * mongo events.
 */
@Component
public class StatisticContentAfterSaveListener extends BasicMongoEventListener<StatisticContent> {

  private final StatisticContentPublicService service;

  private static final String PATH_TEMPLATE = "api/{0}/statistic-content";

  public StatisticContentAfterSaveListener(
      DeliveryNetworkService context, StatisticContentPublicService service) {
    super(context);
    this.service = service;
  }

  /**
   * After saving the document in mongodb then this listener will be called and upload the content
   * to amazon s3 bucket with file name "statistic-content" and path is "api/{0}". {0} indicates
   * placeholder for brand like bma,ladbrokes etc.,
   */
  @Override
  public void onAfterSave(AfterSaveEvent<StatisticContent> event) {
    String brand = event.getSource().getBrand();
    String eventId = event.getSource().getEventId();
    List<StatisticContentDto> content = this.service.findAllByBrandAndEventId(brand, eventId);
    uploadCollection(brand, PATH_TEMPLATE, eventId, content);
  }

  /**
   * After Deleting the document in mongodb. then this listener will be invoked and delete the
   * respective document in s3 bucket and again fetch the remaining documents for the respective
   * eventId and upload them to the s3 as well.
   */
  @Override
  protected void onAfterDelete(
      AfterDeleteEvent<StatisticContent> deleteEvent,
      AfterSaveEvent<StatisticContent> sourceEvent) {
    Document deletedItem = deleteEvent.getSource();
    StatisticContent source = sourceEvent.getSource();
    String sourceId = source.getId();
    Assert.notNull(sourceId, "source id must not be null");
    String deletedId = deletedItem.getObjectId("_id").toHexString();
    Assert.notNull(deletedId, "deleted id must not be null");
    if (sourceId.equalsIgnoreCase(deletedId)) {
      super.onAfterDelete(deleteEvent, sourceEvent);
    }
  }
}
