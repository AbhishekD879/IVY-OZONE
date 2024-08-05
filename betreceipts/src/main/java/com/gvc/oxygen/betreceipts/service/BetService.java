package com.gvc.oxygen.betreceipts.service;

import com.gvc.oxygen.betreceipts.dto.BetDTO;
import com.gvc.oxygen.betreceipts.entity.Bet;
import com.gvc.oxygen.betreceipts.mapping.BetMapper;
import com.gvc.oxygen.betreceipts.repository.BetRepository;
import java.util.List;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.scheduling.annotation.Async;
import org.springframework.stereotype.Service;
import reactor.core.publisher.Flux;

@Slf4j
@Service
@RequiredArgsConstructor
public class BetService {

  private final BetRepository betRepository;

  private final BetMapper betMapper;

  @Async
  public List<BetDTO> saveBets(List<BetDTO> bets, String username) {
    try {
      bets.stream().forEach((BetDTO betDTO) -> betDTO.setUsername(username));
      betMapper.toEntityList(bets).forEach(bet -> this.saveBet(bet, username));

    } catch (Exception ex) {
      log.error("Error while saving bet info ", ex);
    }
    return bets;
  }

  public Iterable<Bet> updateBets(List<Bet> bets) {
    return betRepository.saveAll(bets);
  }

  public Bet saveBet(Bet bet, String username) {
    Bet existingBet = betRepository.findById(username).orElse(null);
    if (existingBet == null) {
      existingBet = bet;
    } else {
      existingBet.getEventIds().addAll(bet.getEventIds());
    }
    betRepository.save(existingBet);
    return bet;
  }

  public Bet findByUsername(String username) {
    return betRepository.findById(username).orElse(null);
  }

  public Flux<Bet> findAllBets() {
    return Flux.fromIterable(betRepository.findAll());
  }
}
