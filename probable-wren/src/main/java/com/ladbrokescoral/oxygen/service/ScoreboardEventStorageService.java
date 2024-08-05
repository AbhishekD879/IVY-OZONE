package com.ladbrokescoral.oxygen.service;

import com.ladbrokescoral.oxygen.dto.scoreboard.FootballJsonEvent;
import java.util.Optional;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.stereotype.Service;

@Service
public class ScoreboardEventStorageService {

  private final ScoreboardCache cache;

  @Autowired
  public ScoreboardEventStorageService(@Qualifier("scoreboardCache") ScoreboardCache cache) {
    this.cache = cache;
  }

  public Optional<String> getInitialData(String eventId) {
    return cache.findById(eventId).map(FootballJsonEvent::getData);
  }
}
