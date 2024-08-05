package com.coral.oxygen.edp.model.mapping.config;

import java.util.HashMap;
import java.util.Map;
import lombok.AccessLevel;
import lombok.NoArgsConstructor;

@NoArgsConstructor(access = AccessLevel.PRIVATE)
public class ModelMarketUtils {
  private static final Map<String, String> marketsColumnsNumberByDispSortName = new HashMap<>();

  static {
    marketsColumnsNumberByDispSortName.put("CS", "2-3");
    marketsColumnsNumberByDispSortName.put("MR", "3");
    marketsColumnsNumberByDispSortName.put("H1", "3");
    marketsColumnsNumberByDispSortName.put("H2", "3");
    marketsColumnsNumberByDispSortName.put("HT", "3");
    marketsColumnsNumberByDispSortName.put("MH", "3");
    marketsColumnsNumberByDispSortName.put("3W", "3");
    marketsColumnsNumberByDispSortName.put("3WFBR", "3");
    marketsColumnsNumberByDispSortName.put("HH", "2");
    marketsColumnsNumberByDispSortName.put("AH", "2");
    marketsColumnsNumberByDispSortName.put("WH", "2");
    marketsColumnsNumberByDispSortName.put("HL", "2");
    marketsColumnsNumberByDispSortName.put("BO", "2-3");
    marketsColumnsNumberByDispSortName.put("GB", "2");
    marketsColumnsNumberByDispSortName.put("TN", "2");
    marketsColumnsNumberByDispSortName.put("NN", "2");
    marketsColumnsNumberByDispSortName.put("2W", "2-3");
    marketsColumnsNumberByDispSortName.put("2WFBR", "2");
    marketsColumnsNumberByDispSortName.put("HF", "3");
    marketsColumnsNumberByDispSortName.put("FS", "3");
    marketsColumnsNumberByDispSortName.put("LS", "3");
    marketsColumnsNumberByDispSortName.put("AG", "3");
    marketsColumnsNumberByDispSortName.put("MG", "3");
    marketsColumnsNumberByDispSortName.put("HS", "3");
    marketsColumnsNumberByDispSortName.put("SC", "3");
    marketsColumnsNumberByDispSortName.put("LC", "3");
    marketsColumnsNumberByDispSortName.put("L1", "1");
    marketsColumnsNumberByDispSortName.put("L2", "2-3");
    marketsColumnsNumberByDispSortName.put("L3", "2-3");
  }

  public static String marketColumnNumber(String dispSortName) {
    return marketsColumnsNumberByDispSortName.get(dispSortName);
  }

  public static String getMarketsColumnsNumberForExceptions(int outcomesCount) {
    return outcomesCount < 6 ? "1" : "2-3";
  }
}
