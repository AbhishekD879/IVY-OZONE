package com.coral.oxygen.middleware.featured.service


import com.coral.oxygen.middleware.common.imdg.DistributedMap
import com.coral.oxygen.middleware.pojos.model.output.EventsModuleData
import com.coral.oxygen.middleware.pojos.model.output.featured.EventsModule
import com.coral.oxygen.middleware.pojos.model.output.featured.FeaturedModel
import com.egalacoral.spark.liveserver.Subscriber
import com.egalacoral.spark.liveserver.service.LiveServerSubscriber
import com.egalacoral.spark.liveserver.service.LiveServerSubscriptionsQAStorage
import spock.lang.Specification

import static com.coral.oxygen.middleware.featured.utils.FeaturedDataUtils.getFeaturedModelFromResource
import static java.util.stream.Collectors.toList

class FeaturedLiveServerSubscriberSpec extends Specification {
  Subscriber subcriber
  DistributedMap<Object, Object> map
  FeaturedLiveServerSubscriber featuredLiveServerSubscriber
  private LiveServerSubscriber liveServerSubscriber

  def setup() {
    subcriber = Mock(Subscriber)
    liveServerSubscriber = Mock(LiveServerSubscriber)
    def lsQaStorageMock = Mock(LiveServerSubscriptionsQAStorage)
    featuredLiveServerSubscriber = new FeaturedLiveServerSubscriber(subcriber, lsQaStorageMock, liveServerSubscriber)
  }


  def "Check featured liveserver subscription method calls"() {
    FeaturedModel featuredModel = getFeaturedModelFromResource("featured_model_for_subscribe.json")
    List<EventsModuleData> eventsModules = featuredModel.getModules().stream()
        .filter({ f -> f instanceof EventsModule })
        .map({ f -> (EventsModule) f })
        .flatMap({m -> m.getData().stream()})
        .collect(toList())
    when:
    featuredLiveServerSubscriber.subscribe(eventsModules)

    then:
    1 * liveServerSubscriber.subscribe(LiveServerSubscriber.EventSubscribeInfo.builder()
        .categoryId(16)
        .id("5229700")
        .market("123")
        .market("333")
        .outcome("222")
        .outcome("444")
        .build())

    1 * liveServerSubscriber.subscribe(LiveServerSubscriber.EventSubscribeInfo.builder()
        .categoryId(1)
        .id("5500622")
        .build())
  }
}
