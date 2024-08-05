package com.oxygen.middleware.common.service.notification

import com.coral.oxygen.middleware.common.service.notification.KafkaPublisher
import com.coral.oxygen.middleware.common.service.notification.MessagePublisher
import com.coral.oxygen.middleware.common.service.notification.topic.TopicResolver
import org.springframework.kafka.core.KafkaTemplate
import org.springframework.scheduling.annotation.AsyncResult
import org.springframework.util.concurrent.ListenableFutureCallback
import spock.lang.Specification

import static com.coral.oxygen.middleware.common.service.notification.topic.TopicType.FEATURED_LIVE_SERVER_MODULES
import static com.coral.oxygen.middleware.common.service.notification.topic.TopicType.FEATURED_MODULE_CONTENT_CHANGED

class KafkaPublisherSpec extends Specification {

  KafkaTemplate<String, String> kafkaTemplate = Mock()

  TopicResolver topicResolver = new TopicResolver("prefix")

  AsyncResult asyncResult = Mock()

  MessagePublisher messagePublisher

  def setup() {
    messagePublisher = new KafkaPublisher(kafkaTemplate, topicResolver)
  }

  def "Send Notification"() {
    when:
    messagePublisher.publish(FEATURED_MODULE_CONTENT_CHANGED, "message")

    then:
    1 * asyncResult.addCallback(_ as ListenableFutureCallback)
    1 * kafkaTemplate.send(topicResolver.find(FEATURED_MODULE_CONTENT_CHANGED), null, "message") >> asyncResult
  }

  def "Send Key-Value Message"() {
    when:
    messagePublisher.publish(FEATURED_LIVE_SERVER_MODULES,"1212", "message")

    then:
    1 * asyncResult.addCallback(_ as ListenableFutureCallback)
    1 * kafkaTemplate.send(topicResolver.find(FEATURED_LIVE_SERVER_MODULES), "1212", "message") >> asyncResult
  }
}
