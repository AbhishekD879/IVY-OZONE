package com.coral.oxygen.middleware.ms.liveserv.impl.redis;

import com.coral.oxygen.middleware.ms.liveserv.model.CachedChannel;
import java.util.List;
import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface SubscriptionCache extends CrudRepository<CachedChannel, String> {

  @Override
  List<CachedChannel> findAll();
}
