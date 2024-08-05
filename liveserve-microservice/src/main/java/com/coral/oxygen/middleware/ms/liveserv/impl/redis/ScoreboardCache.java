package com.coral.oxygen.middleware.ms.liveserv.impl.redis;

import com.coral.oxygen.middleware.ms.liveserv.model.scoreboard.ScoreboardEvent;
import java.util.Optional;
import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface ScoreboardCache extends CrudRepository<ScoreboardEvent, String> {
  @Override
  Optional<ScoreboardEvent> findById(String s);
}
