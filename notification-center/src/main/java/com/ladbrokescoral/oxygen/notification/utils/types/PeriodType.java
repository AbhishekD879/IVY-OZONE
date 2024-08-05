package com.ladbrokescoral.oxygen.notification.utils.types;

import com.ladbrokescoral.oxygen.notification.utils.Type;
import java.util.Collections;
import java.util.List;

public class PeriodType implements Type {
  @Override
  public List<String> channels() {
    return Collections.singletonList("sCLOCK");
  }
}
