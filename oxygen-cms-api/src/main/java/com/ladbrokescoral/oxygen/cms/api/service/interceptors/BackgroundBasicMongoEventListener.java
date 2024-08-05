package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.entity.HasBrand;
import com.ladbrokescoral.oxygen.cms.api.service.cache.DeliveryNetworkService;
import java.util.concurrent.ExecutorService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.data.mongodb.core.mapping.event.AfterSaveEvent;

public abstract class BackgroundBasicMongoEventListener<T extends HasBrand>
    extends BasicMongoEventListener<T> {

  @Autowired
  @Qualifier("cachedThreadPool")
  private ExecutorService executorService;

  protected BackgroundBasicMongoEventListener(DeliveryNetworkService context) {
    super(context);
  }

  @Override
  public void onAfterSave(AfterSaveEvent<T> event) {
    executorService.execute(() -> onAfterSaveInBackground(event));
  }

  protected abstract void onAfterSaveInBackground(AfterSaveEvent<T> event);
}
