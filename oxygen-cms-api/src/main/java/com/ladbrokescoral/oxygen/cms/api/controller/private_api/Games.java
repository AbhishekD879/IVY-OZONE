package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.entity.EventScore;
import com.ladbrokescoral.oxygen.cms.api.entity.EventScoreResponse;
import com.ladbrokescoral.oxygen.cms.api.entity.FileType;
import com.ladbrokescoral.oxygen.cms.api.entity.Game;
import com.ladbrokescoral.oxygen.cms.api.entity.GameEvent;
import com.ladbrokescoral.oxygen.cms.api.service.*;
import java.util.List;
import java.util.Objects;
import javax.validation.Valid;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.multipart.MultipartFile;

@Slf4j
@RestController
public class Games extends AbstractCrudController<Game> {
  private GameService gameService;
  private GameEventService gameEventService;
  private GameScoreService gameScoreService;
  private GamificationService gamificationService;

  Games(
      GameService gameService,
      GameEventService gameEventService,
      GameScoreService gameScoreService,
      GamificationService gamificationService) {
    super(gameService);
    this.gameService = gameService;
    this.gameEventService = gameEventService;
    this.gameScoreService = gameScoreService;
    this.gamificationService = gamificationService;
  }

  @PostMapping("game")
  @Override
  public ResponseEntity create(@RequestBody @Valid Game entity) {
    return super.create(entity);
  }

  @GetMapping("game")
  @Override
  public List<Game> readAll() {
    return super.readAll();
  }

  @GetMapping("game/{id}")
  @Override
  public Game read(@PathVariable String id) {
    return super.read(id);
  }

  @GetMapping("game/brand/{brand}")
  @Override
  public List<Game> readByBrand(@PathVariable String brand) {
    return gameService.findByBrand(brand);
  }

  @PutMapping("game/{id}")
  @Override
  public Game update(@PathVariable String id, @RequestBody @Valid Game entity) {
    if (Objects.nonNull(entity.getSeasonId())) {
      gamificationService.validateGameTeamNameWithSeasonTeamName(entity);
    }
    return super.update(id, entity);
  }

  @DeleteMapping("game/{id}")
  @Override
  public ResponseEntity delete(@PathVariable String id) {
    return super.delete(id);
  }

  @GetMapping("game/brand/{brand}/event-id/{event-id}")
  public ResponseEntity<IncompleteGameEvent> readByEventId(
      @PathVariable String brand, @PathVariable("event-id") String eventId) {
    return gameEventService
        .findByEventId(brand, eventId)
        .map(gameEvent -> new ResponseEntity<>(gameEvent, HttpStatus.OK))
        .orElse(new ResponseEntity<>(HttpStatus.NO_CONTENT));
  }

  @PostMapping("game/{id}/image/event/{eventId}/team/{teamType}")
  public GameEvent uploadImage(
      @PathVariable("id") String id,
      @PathVariable("eventId") String eventId,
      @PathVariable("teamType") String teamType,
      @RequestParam("file") MultipartFile file,
      @RequestParam(value = "fileType", required = false) FileType fileType,
      @RequestParam(value = "fileName", required = false) String fileName) {

    Game game = gameService.findById(id);
    GameEvent gameEvent = gameEventService.getGameEventById(game, eventId);
    gameEventService.uploadGameEventTeamImage(
        gameEvent, teamType, file, fileType, fileName, game.getBrand());
    update(id, game);
    return gameEvent;
  }

  @DeleteMapping("game/{id}/image/event/{eventId}/team/{teamType}")
  public GameEvent removeImage(
      @PathVariable("id") String id,
      @PathVariable("eventId") String eventId,
      @PathVariable("teamType") String teamType) {
    Game game = gameService.findById(id);
    GameEvent gameEvent = gameEventService.getGameEventById(game, eventId);
    gameEventService.removeImage(gameEvent, teamType);
    update(id, game);
    return gameEvent;
  }

  @PostMapping("game/{id}/score")
  public ResponseEntity<EventScoreResponse> updateScore(
      @PathVariable("id") String gameId, @RequestBody EventScore eventScore) {
    log.info("Received score: {} for game: {}", eventScore, gameId);
    return new ResponseEntity<>(gameScoreService.saveScore(gameId, eventScore), HttpStatus.OK);
  }

  @GetMapping("game/{id}/score")
  public List<Integer> getScore(@PathVariable("id") String eventId) {
    return gameScoreService.getScore(eventId);
  }
}
