package com.coral.oxygen.middleware.ms.liveserv.qa;

import com.coral.oxygen.middleware.ms.liveserv.MessageHandler;
import com.coral.oxygen.middleware.ms.liveserv.model.messages.Envelope;
import com.coral.oxygen.middleware.ms.liveserv.model.messages.EventMessageEnvelope;
import com.google.common.cache.Cache;
import com.google.common.cache.CacheBuilder;
import java.util.LinkedList;
import java.util.List;
import java.util.concurrent.TimeUnit;
import javax.annotation.PostConstruct;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

/** Created by azayats on 12.05.17. */
@ConditionalOnProperty(name = "qa.messages.enabled")
@RestController
@RequestMapping(value = "qa/messages", produces = "application/json")
public class QAMessageCollector implements MessageHandler {

  private int maxChannelsCount = 1000;
  private int expireAfterWriteSec = 600;
  private int maxCountPerChannel = 5;

  private Cache<String, List<Envelope>> cache;

  @PostConstruct
  public void initCache() {
    cache =
        CacheBuilder.<String, List<Envelope>>newBuilder()
            .maximumSize(maxChannelsCount)
            .expireAfterWrite(expireAfterWriteSec, TimeUnit.SECONDS)
            .build();
  }

  @Override
  public void handle(EventMessageEnvelope envelope) {
    String channel = envelope.getChannel();
    List<Envelope> list = cache.getIfPresent(channel);
    if (list == null) {
      list = new LinkedList<>();
      cache.put(channel, list);
    }
    list.add(envelope);
    while (list.size() > maxCountPerChannel) {
      list.remove(0);
    }
  }

  @GetMapping(value = "{channel}")
  public List<Envelope> getByChannel( //
      @PathVariable("channel") String channel //
      ) {
    return cache.getIfPresent(channel);
  }

  @Value("${qa.messages.max.channels.count}")
  public void setMaxChannelsCount(int maxChannelsCount) {
    this.maxChannelsCount = maxChannelsCount;
  }

  @Value("${qa.messages.expire.after.write.sec}")
  public void setExpireAfterWriteSec(int expireAfterWriteSec) {
    this.expireAfterWriteSec = expireAfterWriteSec;
  }

  @Value("${qa.messages.max.count.per.channel}")
  public void setMaxCountPerChannel(int maxCountPerChannel) {
    this.maxCountPerChannel = maxCountPerChannel;
  }
}
