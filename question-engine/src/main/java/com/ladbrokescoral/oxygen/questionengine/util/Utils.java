package com.ladbrokescoral.oxygen.questionengine.util;

import lombok.experimental.UtilityClass;

import java.util.ArrayList;
import java.util.Collection;
import java.util.List;
import java.util.stream.Collectors;

@UtilityClass
public class Utils {
  private static final int CAPITALIZED_ALPHABET_ASCII_SHIFT = 65;

  public static <T> Collection<? extends Collection<T>> splitIntoBatches(Collection<T> list, int batchSize) {

    List<List<T>> batches = new ArrayList<>();

    if (batchSize > list.size()) {
      batches.add(new ArrayList<>(list));
    } else {
      List<T> currentBatch;
      while (!(currentBatch = nextBatches(list, batchSize, batches)).isEmpty()) {
        batches.add(currentBatch);
      }
    }
    return batches;
  }

  public static String toAlphabeticRepresentation(int number) {
    return toAlphabeticRepresentation(number, "");
  }

  public static int fromAlphabeticRepresentation(char alphabetic) {
    return ((int) alphabetic) - CAPITALIZED_ALPHABET_ASCII_SHIFT;
  }

  private static boolean isWithinEnglishAlphabet(int number) {
    return number >= 0 && number <= 25;
  }

  private static String toAlphabeticRepresentation(int number, String collectedLetters) {
    if (number < 0) {
      throw new IllegalArgumentException("Expected positive number, actual: " + number);
    }
    if (!isWithinEnglishAlphabet(number)) {
      int aLetterCode = 0;
      int zLetterCode = 25;
      return collectedLetters + toAlphabeticRepresentation(number - zLetterCode, String.valueOf((char) (aLetterCode + CAPITALIZED_ALPHABET_ASCII_SHIFT)));
    }
    return collectedLetters + (char) (number + CAPITALIZED_ALPHABET_ASCII_SHIFT);
  }

  private static <T> List<T> nextBatches(Collection<T> list, int batchSize, List<List<T>> batches) {
    return list.stream()
        .skip((long) batches.size() * batchSize)
        .limit(batchSize)
        .collect(Collectors.toList());
  }
}
