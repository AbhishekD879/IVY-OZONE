package com.ladbrokescoral.oxygen.cms.api.service.public_api;

import com.ladbrokescoral.oxygen.cms.api.dto.GameDto;
import com.ladbrokescoral.oxygen.cms.api.entity.Game;
import com.ladbrokescoral.oxygen.cms.api.mapping.GameMapper;
import com.ladbrokescoral.oxygen.cms.api.service.GameService;
import java.util.ArrayList;
import java.util.List;
import java.util.Objects;
import java.util.stream.Collectors;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
@Slf4j
public class GamePublicService {
  private final GameService gameService;

  public List<GameDto> findByBrand(String brand) {
    return gameService.findByBrand(brand).stream()
        .filter(Game::isEnabled)
        .map(GameMapper.getInstance()::toDto)
        .collect(Collectors.toList());
  }

  public GameDto getSingleByBrand(String brand, GameState gameState, String gameId) {
    if (gameId != null) {
      return GameMapper.getInstance().toDto(gameService.findById(gameId));
    } else if (gameState != null) {
      switch (gameState) {
        case ACTIVE:
          return GameMapper.getInstance().toDto(gameService.getActiveGame(brand));
        case BEFORE_ACTIVE:
          return GameMapper.getInstance().toDto(gameService.getPreviouslyActiveGame(brand));
        default:
          throw new IllegalArgumentException(
              String.format("Game State '%s' is not supported", gameState));
      }
    }
    throw new IllegalArgumentException(
        String.format("Game State '%s' and game id '%s' is not supported", gameState, gameId));
  }

  public List<GameDto> findPreviousCurrentAndFutureGameByBrand(String brand) {
    List<GameDto> games = new ArrayList<>();
    GameDto previousGame =
        GameMapper.getInstance().toDto(gameService.getPreviouslyActiveGame(brand));
    if (Objects.nonNull(previousGame.getId())) {
      games.add(previousGame);
    }
    games.addAll(findCurrentAndFutureGameByBrand(brand));
    return games;
  }

  public List<GameDto> findCurrentAndFutureGameByBrand(String brand) {
    GameDto activeGame = null;
    try {
      activeGame = GameMapper.getInstance().toDto(gameService.getActiveGame(brand));
    } catch (Exception ex) {
      log.error(ex.getMessage());
    }
    List<GameDto> futureGames =
        gameService.getFutureActiveGames(brand).stream()
            .map(game -> GameMapper.getInstance().toDto(game))
            .collect(Collectors.toList());
    if (Objects.nonNull(activeGame) && !futureGames.contains(activeGame)) {
      futureGames.add(activeGame);
    }
    return futureGames;
  }
}
