package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import static java.text.MessageFormat.format;

import com.ladbrokescoral.oxygen.cms.api.entity.HasBrand;
import com.ladbrokescoral.oxygen.cms.api.service.cache.DeliveryNetworkService;
import java.util.List;
import java.util.Map;
import java.util.Objects;
import java.util.Optional;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.mongodb.core.mapping.event.AbstractMongoEventListener;
import org.springframework.data.mongodb.core.mapping.event.AfterConvertEvent;
import org.springframework.data.mongodb.core.mapping.event.AfterDeleteEvent;
import org.springframework.data.mongodb.core.mapping.event.AfterSaveEvent;

@Slf4j
public abstract class BasicMongoEventListener<E extends HasBrand>
    extends AbstractMongoEventListener<E> {

  protected static final String EMPTY_CONTENT = "";
  private DeliveryNetworkService context;

  protected BasicMongoEventListener(DeliveryNetworkService context) {
    this.context = context;
  }

  // FIXME: should be: <U extends Collection<T>> or BasicMongoEventListener<DTO, ENTITY>
  protected <U extends List<?>> void uploadCollection(
      String brand, String pathTemplate, String fileName, U content) {
    if (Objects.isNull(content)) {
      log.error("Can't publish content for " + fileName + " due to the empty data structure");
    } else {
      context.upload(brand, format(pathTemplate, brand), fileName, content);
    }
  }

  // FIXME: should be: <U extends Map<String, T>> or BasicMongoEventListener<DTO, ENTITY>
  protected <U extends Map<String, ?>> void uploadMap(
      String brand, String pathTemplate, String fileName, U content) {
    if (Objects.isNull(content) || content.isEmpty()) {
      log.error("Can't publish content for " + fileName + " due to the empty data structure");
    } else {
      context.upload(brand, format(pathTemplate, brand), fileName, content);
    }
  }

  // FIXME: should be: Optional<T> or BasicMongoEventListener<DTO, ENTITY>
  protected void uploadOptional(
      String brand, String pathTemplate, String fileName, Optional<?> content) {
    if (!content.isPresent()) {
      log.error("Can't publish content for leagues due to the empty data structure");
    } else {
      context.upload(brand, format(pathTemplate, brand), fileName, content.get());
    }
  }

  protected void uploadCFContent(
      String brand, String pathTemplate, String fileName, Optional<?> content) {
    if (!content.isPresent()) {
      log.error("Can't publish content for leagues due to the empty data structure");
    } else {
      context.uploadCFContent(brand, format(pathTemplate, brand), fileName, content.get());
    }
  }

  protected void delete(String brand, String pathTemplate, String fileName) {
    context.delete(brand, format(pathTemplate, brand), fileName);
  }

  private AfterSaveEvent<E> afterSaveEvent;

  @Override
  public void onAfterConvert(AfterConvertEvent<E> event) {
    afterSaveEvent =
        new AfterSaveEvent<>(event.getSource(), event.getDocument(), event.getCollectionName());
  }

  @Override
  public void onAfterDelete(AfterDeleteEvent<E> event) {
    onAfterDelete(event, afterSaveEvent);
  }

  protected void onAfterDelete(AfterDeleteEvent<E> deleteEvent, AfterSaveEvent<E> sourceEvent) {
    onAfterSave(sourceEvent);
  }
}
