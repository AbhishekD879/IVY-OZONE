package com.ladbrokescoral.oxygen.notification.utils.types;

import com.ladbrokescoral.oxygen.notification.utils.Type;
import java.util.Collections;
import java.util.List;
import lombok.extern.slf4j.Slf4j;

@Slf4j
public class UnknownType implements Type {

  private final String type;

  public UnknownType(String type) {
    this.type = type;
  }

  @Override
  public List<String> channels() {
    return Collections.emptyList();
  }
}
