package com.ladbrokescoral.cashout.repository;

import java.math.BigInteger;
import lombok.Data;

@Data
public class EntityStatus {
  private final BigInteger entityId;
  private final boolean active;
}
