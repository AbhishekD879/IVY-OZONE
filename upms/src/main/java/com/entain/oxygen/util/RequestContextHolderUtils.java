package com.entain.oxygen.util;

import com.entain.oxygen.exceptions.UserNotFoundException;
import lombok.experimental.UtilityClass;
import org.apache.commons.lang3.ObjectUtils;
import reactor.util.context.Context;
import reactor.util.context.ContextView;

@UtilityClass
public class RequestContextHolderUtils {

  private static final String USERNAME = "user";

  public static Context putTokenInContext(Context context, String username) {
    return context.put(USERNAME, username);
  }

  public static String getSportsBookUser(ContextView context) throws UserNotFoundException {
    return context
        .getOrEmpty(RequestContextHolderUtils.USERNAME)
        .filter(ObjectUtils::isNotEmpty)
        .map(Object::toString)
        .orElseThrow(() -> new UserNotFoundException("user not found in context"));
  }
}
