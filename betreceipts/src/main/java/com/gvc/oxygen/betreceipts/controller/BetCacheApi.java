package com.gvc.oxygen.betreceipts.controller;

import com.coral.bpp.api.model.bet.api.response.UserDataResponse;
import com.coral.bpp.api.service.BppApiAsync;
import com.gvc.oxygen.betreceipts.dto.TipDTO;
import com.gvc.oxygen.betreceipts.entity.NextRacesResult;
import com.gvc.oxygen.betreceipts.service.BetService;
import com.gvc.oxygen.betreceipts.service.NextRacesPublicService;
import javax.validation.Valid;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestHeader;
import org.springframework.web.bind.annotation.RestController;
import reactor.core.publisher.Mono;

@RestController
@RequiredArgsConstructor
@Slf4j
@Validated
public class BetCacheApi implements Public {

  private final BetService betService;

  private final NextRacesPublicService nextRacesPublicService;

  private final BppApiAsync bppApiAsync;

  @PostMapping("/bets")
  public Mono<NextRacesResult> saveAll(
      @Valid @RequestBody TipDTO bets, @RequestHeader String token) {
    return bppApiAsync
        .getUserData(token)
        .map((UserDataResponse user) -> getNextRaces(user.getSportBookUserName(), bets));
  }

  private NextRacesResult getNextRaces(String username, TipDTO bets) {

    betService.saveBets(bets.getBets(), username);
    return nextRacesPublicService.find(username, bets.isTipEnabled());
  }
}
