package com.gvc.oxygen.betreceipts.entity;

import java.util.HashSet;
import java.util.Set;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.NoArgsConstructor;
import org.springframework.data.annotation.Id;
import org.springframework.data.redis.core.RedisHash;

@Data
@EqualsAndHashCode
@RedisHash("bets")
@AllArgsConstructor
@NoArgsConstructor
public class Bet {
  @Id private String username;
  private Set<String> eventIds = new HashSet<>();
}
