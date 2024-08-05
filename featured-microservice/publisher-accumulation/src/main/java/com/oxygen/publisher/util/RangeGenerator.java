package com.oxygen.publisher.util;

import java.util.ArrayList;
import java.util.List;
import lombok.extern.slf4j.Slf4j;
import org.springframework.util.ObjectUtils;

/**
 * Convert s1m1-s2m3 string to list s1m1,s1m2,s1m3,s2m1,s2m2,s2m3
 *
 * @author Vitalij Havryk
 */
@Slf4j
public class RangeGenerator {

  public List<String> generate(String rangeString) {
    checkRange(rangeString);
    Range range = getRange(rangeString);
    return range.toList();
  }

  private Range getRange(String rangeString) {
    int delimiterIndex = checkValidRange(rangeString);
    String startRange = rangeString.substring(0, delimiterIndex);
    String endRange = rangeString.substring(delimiterIndex + 1);
    log.info("Use range : {}-{}", startRange, endRange);
    Range range = new Range();
    setStartRangeData(startRange, range);
    setEndRangeData(range, endRange);

    if (!range.valid()) {
      throwException("Invalid range format");
    }
    return range;
  }

  private void setEndRangeData(Range range, String endRange) {
    RangeScanner scanner = new RangeScanner(endRange);
    while (scanner.hasNext()) {
      scanner.next();
      range.endIndexes.add(scanner.nextInt());
    }
  }

  private void setStartRangeData(String startRange, Range range) {
    RangeScanner scanner = new RangeScanner(startRange);
    while (scanner.hasNext()) {
      String key = scanner.next();
      Integer startIndex = scanner.nextInt();
      range.keyValues.add(new KeyValue(key, startIndex));
    }
  }

  private int checkValidRange(String rangeString) {
    int indexOf = rangeString.indexOf("-");
    if (indexOf > rangeString.length() - 2) {
      throw new IllegalArgumentException("Invalid range format");
    }
    return indexOf;
  }

  private void checkRange(String rangeString) {
    if (ObjectUtils.isEmpty(rangeString)) {
      throwException("range is null");
    }
    if (!rangeString.contains("-")) {
      throwException("range doesn't contain '-'");
    }
  }

  private void throwException(String message) {
    throw new IllegalArgumentException(
        message + " . Please provide startIndex in format : s1m1-s2m3");
  }

  public static class Range {

    private static final String ROOT_ID = "";
    private List<Integer> endIndexes = new ArrayList<>();
    private List<KeyValue> keyValues = new ArrayList<>();

    public boolean valid() {
      return keyValues.size() == endIndexes.size();
    }

    public List<String> toList() {
      List<String> ids = new ArrayList<>();
      populateList(0, ids, ROOT_ID);
      return ids;
    }

    public void populateList(int index, List<String> ids, String rootId) {
      int start = keyValues.get(index).startIndex;
      String key = keyValues.get(index).key;
      int end = endIndexes.get(index);
      int nextIndex = index + 1;
      for (int k = start; k <= end; k = k + 1) {
        String id = rootId + key + k;
        if (nextIndex != keyValues.size()) {
          populateList(nextIndex, ids, id);
        } else {
          ids.add(id);
        }
      }
    }
  }

  private static class KeyValue {

    KeyValue(String key, Integer value) {
      this.key = key;
      this.startIndex = value;
    }

    private String key;
    private Integer startIndex;
  }
}
