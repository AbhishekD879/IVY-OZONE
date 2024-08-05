package com.ladbrokescoral.oxygen.timeline.api.registrators;

import com.ladbrokescoral.oxygen.timeline.api.config.AbstractServiceRegistry;
import lombok.ToString;
import lombok.extern.slf4j.Slf4j;
import org.springframework.context.ConfigurableApplicationContext;

@ToString
@Slf4j
public class TimelineServiceRegistry extends AbstractServiceRegistry {

  public TimelineServiceRegistry(ConfigurableApplicationContext appContext) {
    super(appContext, new Class[] {PagePublisherChannelRegistrator.class});
  }

  public PagePublisherChannelRegistrator getPagePublisherChannelRegistrator() {
    return super.getServiceAndReloadFailed(PagePublisherChannelRegistrator.class);
  }
}
