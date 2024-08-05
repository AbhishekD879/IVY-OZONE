package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.entity.Game;
import com.ladbrokescoral.oxygen.cms.api.entity.GameEvent;
import com.ladbrokescoral.oxygen.cms.api.exception.ActiveGameNotFoundException;
import com.ladbrokescoral.oxygen.cms.api.exception.NotFoundException;
import com.ladbrokescoral.oxygen.cms.api.repository.GameRepository;
import java.time.Instant;
import java.util.Comparator;
import java.util.List;
import java.util.Objects;
import java.util.stream.Collectors;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.domain.Sort;
import org.springframework.stereotype.Service;

@Slf4j
@Service
public class GameService extends AbstractService<Game> {

  private final GameRepository gameRepository;

  public GameService(GameRepository gameRepository) {
    super(gameRepository);
    this.gameRepository = gameRepository;
  }

  @Override
  public Game save(Game entity) {
    if (gamesWithinSameTimeRangeExist(entity)) {
      throw new IllegalArgumentException(
          "Only one active Game can be configured at the same time range. Please change time frame");
    }
    sortEventsByStartDate(entity);
    return gameRepository.save(entity);
  }

  private void sortEventsByStartDate(Game game) {
    if (game != null && game.getEvents() != null) {
      game.setEvents(
          game.getEvents().stream()
              .filter(Objects::nonNull)
              .sorted(
                  Comparator.comparing(
                      GameEvent::getStartTime, Comparator.nullsLast(Comparator.naturalOrder())))
              .collect(Collectors.toList()));
    }
  }

  private boolean gamesWithinSameTimeRangeExist(Game entity) {
    return entity.isEnabled()
        && entity.getDisplayFrom() != null
        && entity.getDisplayTo() != null
        && !gameRepository
            .findByDisplayFromIsBeforeAndDisplayToIsAfterAndBrandIsAndEnabledIsTrueAndIdNot(
                entity.getDisplayTo(), entity.getDisplayFrom(), entity.getBrand(), entity.getId())
            .isEmpty();
  }

  @Override
  public List<Game> findByBrand(String brand) {
    return gameRepository.findByBrand(brand, Sort.by(Sort.Direction.DESC, "displayFrom"));
  }

  public Game getActiveGame(String brand) {
    List<Game> activeGames =
        gameRepository.findByDisplayFromIsBeforeAndDisplayToIsAfterAndBrandIsAndEnabledIsTrue(
            Instant.now(), Instant.now(), brand);

    if (activeGames.isEmpty()) {
      throw new ActiveGameNotFoundException();
    } else if (activeGames.size() > 1) {
      log.error("Expected only one active game, actual: {}", activeGames.size());
    }
    return activeGames.get(0);
  }

  public List<Game> getFutureActiveGames(String brand) {
    return gameRepository.findByDisplayFromIsGreaterThanEqualAndBrandIsAndEnabledIsTrue(
        Instant.now(), brand);
  }

  public Game getPreviouslyActiveGame(String brand) {
    List<Game> game = gameRepository.findLastBeforeActive(brand);
    return !game.isEmpty() ? game.get(0) : new Game();
  }

  public Game findById(String id) {
    return gameRepository.findById(id).orElseThrow(NotFoundException::new);
  }
}
