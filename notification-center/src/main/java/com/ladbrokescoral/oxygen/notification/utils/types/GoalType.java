package com.ladbrokescoral.oxygen.notification.utils.types;

import com.ladbrokescoral.oxygen.notification.utils.Type;
import java.util.Arrays;
import java.util.List;

public class GoalType implements Type {
  @Override
  public List<String> channels() {
    return Arrays.asList("sEVENT", "sICENT", "sSCBRD");
  }
}
