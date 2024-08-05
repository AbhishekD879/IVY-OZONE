package com.ladbrokescoral.oxygen.betpackmp.controller;

import static com.ladbrokescoral.oxygen.betpackmp.constants.BetPackConstants.ACTIVE_BET_PACK_IDS;

import com.ladbrokescoral.oxygen.betpackmp.redis.ActiveBetPacks;
import com.ladbrokescoral.oxygen.betpackmp.redis.BetPackRedisService;
import com.ladbrokescoral.oxygen.betpackmp.redis.bet_pack.BetPackMessage;
import com.ladbrokescoral.oxygen.betpackmp.redis.bet_pack.BetPackRedisOperationsImpl;
import java.util.List;
import java.util.Objects;
import java.util.Optional;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.util.HtmlUtils;

/** Created by Rakesh Bonu on 26.07.22. */
@RestController
public final class RedisDataController {

  private final BetPackRedisService betPackRedisService;

  private final BetPackRedisOperationsImpl betPackRedisOperations;

  public RedisDataController(
      BetPackRedisService betPackRedisService, BetPackRedisOperationsImpl betPackRedisOperations) {
    this.betPackRedisService = betPackRedisService;
    this.betPackRedisOperations = betPackRedisOperations;
  }

  @GetMapping("/active-bet-packs")
  public ResponseEntity<List<String>> getActiveBetPacks() {
    ActiveBetPacks activeBetPacks = betPackRedisService.getActiveBetPacks(ACTIVE_BET_PACK_IDS);
    List<String> activeBetPackIds = null;
    if (Objects.nonNull(activeBetPacks)) {
      activeBetPackIds = activeBetPacks.getActiveBetPacksIds();
    }
    return new ResponseEntity<>(activeBetPackIds, HttpStatus.OK);
  }

  @GetMapping("/bet-pack/{id}")
  public ResponseEntity<BetPackMessage> getBetPackById(@PathVariable("id") String betPackId) {
    Optional<BetPackMessage> betPackMessage = betPackRedisOperations.getLastSavedMessage(betPackId);
    if (betPackMessage.isPresent()) {
      BetPackMessage sanitizedMessage = sanitizeBetPackMessage(betPackMessage.get());
      return new ResponseEntity<>(sanitizedMessage, HttpStatus.OK);
    } else {
      return new ResponseEntity<>(HttpStatus.NOT_FOUND);
    }
  }

  @GetMapping("/bet-packs")
  public ResponseEntity<List<BetPackMessage>> getBetPackById() {
    List<BetPackMessage> betPackMessage = betPackRedisOperations.getAll();
    return new ResponseEntity<>(betPackMessage, HttpStatus.OK);
  }

  private BetPackMessage sanitizeBetPackMessage(BetPackMessage betPackMessage) {
    betPackMessage.setBetPackId(HtmlUtils.htmlEscape(betPackMessage.getBetPackId()));
    return betPackMessage;
  }
}
