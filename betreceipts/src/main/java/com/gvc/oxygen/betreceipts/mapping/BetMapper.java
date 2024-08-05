package com.gvc.oxygen.betreceipts.mapping;

import com.gvc.oxygen.betreceipts.dto.BetDTO;
import com.gvc.oxygen.betreceipts.entity.Bet;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.StreamSupport;
import org.modelmapper.ModelMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

@Component
public class BetMapper {

  @Autowired private ModelMapper modelMapper;

  public BetDTO toDto(Bet entity) {
    return modelMapper.map(entity, BetDTO.class);
  }

  public Bet toEntity(BetDTO betDTO) {
    Bet bet = modelMapper.map(betDTO, Bet.class);
    bet.getEventIds().add(betDTO.getEventId());
    return bet;
  }

  public Iterable<Bet> toEntityList(List<BetDTO> betDTOS) {
    return betDTOS.stream().map(this::toEntity).collect(Collectors.toList());
  }

  public List<BetDTO> toDtoList(Iterable<Bet> bets) {
    return StreamSupport.stream(bets.spliterator(), false)
        .map(this::toDto)
        .collect(Collectors.toList());
  }
}
