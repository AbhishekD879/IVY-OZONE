package com.ladbrokescoral.oxygen.cms.api.entity;

public class Patterns {
  /**
   * Used to validate vipLevelsInput field Represent comma separated and/or hyphened numbers (spaces
   * are allowed in any position) Matches: 1 or 1,2,3 or 1-23 or 12,3,4,12,2-4,3-4,2 , 4
   */
  static final String VIP_LEVELS_INPUT_PATTERN =
      "^\\s*$|((\\s*\\d\\s*\\,\\s*(?=\\s*\\d\\s*))|(\\s*\\d\\s*\\-(?=\\s*\\d\\s*))|\\s*\\d\\s*)+";

  /** Used to validate comma separated numbers Matches: 1 or 1,2,3 or 10,20,30 etc. */
  public static final String COMMA_SEPARTED_NUMBERS = "^[0-9]+(\\,[0-9]+)*$";

  /** Used to validate comma separated word Matches: ab1 or 1ab4,dfg,xc etc. */
  public static final String COMMA_SEPARTED_WORDS = "\\S*(\\,\\S+)*$";

  private Patterns() {}
}
