package com.ladbrokescoral.oxygen.service;

import com.ladbrokescoral.oxygen.dto.scoreboard.FootballJsonEvent;
import java.util.Optional;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;

@Qualifier("scoreboardCache")
@Repository
public interface ScoreboardCache extends CrudRepository<FootballJsonEvent, String> {
  @Override
  Optional<FootballJsonEvent> findById(String s);
}
