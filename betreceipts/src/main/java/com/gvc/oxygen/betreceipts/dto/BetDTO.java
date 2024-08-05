package com.gvc.oxygen.betreceipts.dto;

import java.io.Serializable;
import java.time.Instant;
import javax.validation.constraints.Pattern;
import lombok.Data;
import lombok.EqualsAndHashCode;

@Data
@EqualsAndHashCode(of = {"eventId", "username"})
public class BetDTO implements Serializable {

  @Pattern(regexp = "[0-9]+")
  private String eventId;

  private Instant startTime;

  // @NotBlank
  private String username;
}
