package com.ladbrokescoral.reactions.util;

import com.ladbrokescoral.reactions.exception.BadRequestException;

/**
 * @author PBalarangakumar 27-06-2023
 */
@SuppressWarnings("unused")
public class ValidationHelper<T> {

  private ValidationHelper() {}

  public static <T> void notNull(final T filed, final T nameOfFiled) {

    if (filed == null) {
      throw new BadRequestException("The " + nameOfFiled + " must be present.");
    }
  }
}
