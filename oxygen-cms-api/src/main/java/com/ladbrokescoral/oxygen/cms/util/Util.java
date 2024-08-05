package com.ladbrokescoral.oxygen.cms.util;

import com.amazonaws.auth.AWSCredentialsProvider;
import com.amazonaws.auth.AWSStaticCredentialsProvider;
import com.amazonaws.auth.BasicAWSCredentials;
import com.amazonaws.auth.DefaultAWSCredentialsProviderChain;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.SerializationFeature;
import com.fasterxml.jackson.datatype.jsr310.JavaTimeModule;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collection;
import java.util.List;
import java.util.UUID;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import java.util.stream.Collectors;
import java.util.stream.Stream;
import lombok.AccessLevel;
import lombok.NoArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.apache.commons.lang3.StringUtils;

@Slf4j
@NoArgsConstructor(access = AccessLevel.PRIVATE)
public class Util {

  private static final Pattern OBJECT_ID_PATTERN = Pattern.compile("^[0-9a-fA-F]{24,32}$");
  private static final Pattern HYPHENATED_NUMBERS_PATTERN =
      Pattern.compile("([0-9]+)\\s*-\\s*([0-9]+)"); // e.x 1-4 or 23-43 or 55 - 1
  private static final String ACCESS_S3_KEY_ENV_VAR = "AWS_S3_ACCESS_KEY_ID";
  private static final String SECRET_S3_KEY_ENV_VAR = "AWS_S3_SECRET_ACCESS_KEY";

  public static String updateBrand(String brand) {
    return brand.equals("retail") ? "connect" : brand;
  }

  public static boolean isValidObjectIdString(String createdBy) {
    return OBJECT_ID_PATTERN.matcher(createdBy).matches();
  }

  public static String randomUUID() {
    return UUID.randomUUID().toString().replace("-", "");
  }
  /**
   * @param input String with comma separated or hyphenated numbers. E.g: 1,2 or 34,5,1-3, or
   *     12-1,0,0-1,5 or 5 or 10-0
   * @return sorted list of parsed integers without duplicates
   */
  public static List<Integer> hyphenatedAndCommaSeparatedNumbersToList(String input) {
    Matcher matcher = HYPHENATED_NUMBERS_PATTERN.matcher(input);
    String result = input;

    while (matcher.find()) {
      String left = matcher.group(1); // If matcher = 3-4, then matcher.group(1) = 3
      String right = matcher.group(2); // If matcher = 3-4, then matcher.group(2) = 4
      String hyphenatedNumbers = matcher.group(); // If matcher = 3-4, then matcher.group() = 3-4
      String commaSeparatedNumbers =
          intRangeToCommaSeparated(Integer.valueOf(left), Integer.valueOf(right));
      result = result.replace(hyphenatedNumbers, commaSeparatedNumbers);
    }
    return Arrays.stream(result.replace(" ", "").split(","))
        .map(Integer::valueOf)
        .distinct()
        .sorted()
        .collect(Collectors.toList());
  }

  /**
   * *
   *
   * @param left - left side of range. E.g. Range: 2-4 left value:2
   * @param right - right side of range. E.g. Range: 2-4 right value:4
   * @return comma separated numbers between left and right values in ASC order. E.g. left=2,
   *     right=4, output: 2,3,4
   */
  private static String intRangeToCommaSeparated(Integer left, Integer right) {
    Integer lower = Math.min(left, right);
    Integer upper = Math.max(left, right);
    StringBuilder builder = new StringBuilder(lower.toString());
    while (++lower <= upper) {
      builder.append(",").append(lower.toString());
    }
    return builder.toString();
  }

  public static List<String> toList(String commaSeparated) {
    return Arrays.asList(commaSeparated.split(","));
  }

  public static List<String> listDiff(List<String> minuend, List<String> subtrahend) {
    return minuend.stream()
        .filter(element -> !subtrahend.contains(element))
        .collect(Collectors.toList());
  }

  @SafeVarargs
  public static <T> List<T> mergeLists(List<? extends T>... lists) {
    return Stream.of(lists)
        .flatMap(Collection::stream)
        .collect(Collectors.toCollection(ArrayList::new));
  }

  public static <T> String join(CharSequence delimiter, Collection<T> collection) {
    return collection.stream().map(String::valueOf).collect(Collectors.joining(delimiter));
  }

  public static <T> boolean isOneOf(T elementToCheck, T... array) {
    return Arrays.asList(array).contains(elementToCheck);
  }

  public static void runForever(Runnable runner) {
    while (!Thread.currentThread().isInterrupted()) {
      runner.run();
    }
  }

  public static ObjectMapper objectMapper() {
    return new ObjectMapper()
        .registerModule(new JavaTimeModule())
        .disable(SerializationFeature.WRITE_DATES_AS_TIMESTAMPS);
  }

  public static AWSCredentialsProvider awsS3CredentialsProvider() {
    String accessKeyId = StringUtils.trim(System.getenv(ACCESS_S3_KEY_ENV_VAR));
    String secretKeyId = StringUtils.trim(System.getenv(SECRET_S3_KEY_ENV_VAR));

    return (accessKeyId != null)
        ? new AWSStaticCredentialsProvider(new BasicAWSCredentials(accessKeyId, secretKeyId))
        : new DefaultAWSCredentialsProviderChain();
  }
}
