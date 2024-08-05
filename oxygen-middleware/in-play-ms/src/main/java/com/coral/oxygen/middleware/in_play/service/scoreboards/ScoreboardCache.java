package com.coral.oxygen.middleware.in_play.service.scoreboards;

import java.util.Optional;
import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface ScoreboardCache extends CrudRepository<ScoreboardEvent, String> {

  @Override
  Optional<ScoreboardEvent> findById(String id);
}
