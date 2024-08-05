package com.gvc.oxygen.betreceipts.dto;

import java.io.Serializable;
import java.util.List;
import javax.validation.Valid;
import lombok.Data;

@Data
public class TipDTO implements Serializable {
  private boolean isTipEnabled;

  private List<@Valid BetDTO> bets;
}
