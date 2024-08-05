package com.coral.oxygen.edp.model.mapping.converter;

import static java.util.stream.Collectors.toList;

import com.coral.oxygen.edp.model.output.OutputMarket;
import java.util.Collection;
import java.util.Comparator;
import java.util.HashMap;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.function.Function;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import java.util.stream.Collectors;
import java.util.stream.Stream;

/**
 * Converts list of markets into collection of groups. Each group is a list of markets with similar
 * marketTemplateName
 */
public class MarketGroupAndSortConverter
    implements Converter<List<OutputMarket>, Collection<List<OutputMarket>>> {

  private static final Map<String, String> TEMPLATE_NAME_TO_SIMPLE_GROUP_KEY_REGEX =
      new HashMap<>();

  static {
    putSimpleGroup("mraoug", "Match Result (and|&) Over/Under .* Goals");
    putSimpleGroup("bttsaoug", "Both Teams to Score (and|&) Over/Under .* Goals");
    putSimpleGroup("ts", ".*[Tt]eam [Ss]pecials.*");
    putSimpleGroup("ps", ".*[Pp]layer [Ss]pecials \\(O/U\\).*");
    putSimpleGroup("ms", ".*[Mm]atch [Ss]pecial.*");
    putSimpleGroup("is", ".*[Ii]n[\\s]*[-]*[Pp]lay [Ss]pecials.*");
    putSimpleGroup("yc", ".*[Yy]our[Cc]all.*");
    putSimpleGroup("fhaoug", "First Half (and|&) Over/Under .* Goals");
    putSimpleGroup("shaoug", "Second Half (and|&) Over/Under .* Goals");
    putSimpleGroup("hmr", "Handicap Match Result.*");
    putSimpleGroup("hfh", "Handicap First Half.*");
    putSimpleGroup("hsh", "Handicap Second Half.*");
    putSimpleGroup("outg", "Over[\\s]*/[\\s]*Under Total Goals .*");
    putSimpleGroup("oufh", "Over[\\s]*/[\\s]*Under First Half \\d+.*");
    putSimpleGroup("oush", "Over[\\s]*/[\\s]*Under Second Half \\d+.*");
  }

  private static void putSimpleGroup(String key, String value) {
    TEMPLATE_NAME_TO_SIMPLE_GROUP_KEY_REGEX.put(key, value);
  }

  private static final Map<String, String> TEMPLATE_NAME_TO_COMPLEX_GROUP_KEY_REGEX =
      new HashMap<>();

  static {
    putComplexGroup("outg", "Over[\\s]*/[\\s]*Under (.*) Total Goals (.*)");
    putComplexGroup("oufh", "Over[\\s]*/[\\s]*Under First Half (.*) (\\d+.*)");
    putComplexGroup("oush", "Over[\\s]*/[\\s]*Under Second Half (.*) (\\d+.*)");
  }

  private static void putComplexGroup(String key, String value) {
    TEMPLATE_NAME_TO_COMPLEX_GROUP_KEY_REGEX.put(key, value);
  }

  @Override
  public Collection<List<OutputMarket>> convert(List<OutputMarket> markets) {

    Stream<OutputMarket> sortedMarkets = sortByDisplayOrder(markets.stream());
    return groupByTemplateMarketName(sortedMarkets);
  }

  private Stream<OutputMarket> sortByDisplayOrder(Stream<OutputMarket> markets) {
    return markets.sorted(
        Comparator.comparing(
                OutputMarket::getDisplayOrder, Comparator.nullsLast(Comparator.naturalOrder()))
            .thenComparing(OutputMarket::getId, Comparator.nullsLast(Comparator.naturalOrder())));
  }

  private Collection<List<OutputMarket>> groupByTemplateMarketName(Stream<OutputMarket> markets) {
    return markets
        .collect(Collectors.groupingBy(generateGroupKeyFunction, LinkedHashMap::new, toList()))
        .values();
  }

  private Function<OutputMarket, String> generateGroupKeyFunction =
      market -> {
        Optional<String> key = generateSimpleKeyByRegex(market);
        if (!key.isPresent()) {
          key = generateComplexKeyByRegexAndTeamName(market);
        }
        return key.orElseGet(() -> generateDefaultKey(market));
      };

  private Optional<String> generateSimpleKeyByRegex(OutputMarket market) {
    return TEMPLATE_NAME_TO_SIMPLE_GROUP_KEY_REGEX.entrySet().stream()
        .filter(entry -> market.getTemplateMarketName().matches(entry.getValue()))
        .map(Map.Entry::getKey)
        .findFirst();
  }

  private Optional<String> generateComplexKeyByRegexAndTeamName(OutputMarket market) {
    return TEMPLATE_NAME_TO_COMPLEX_GROUP_KEY_REGEX.entrySet().stream()
        .map(entry -> generateComplexKeyByEntry(entry, market))
        .filter(Optional::isPresent)
        .map(Optional::get)
        .findFirst();
  }

  private Optional<String> generateComplexKeyByEntry(
      Map.Entry<String, String> entry, OutputMarket market) {
    Pattern pattern = Pattern.compile(entry.getValue());
    Matcher matcher = pattern.matcher(market.getTemplateMarketName());
    if (matcher.find()) {
      return Optional.of(entry.getKey() + matcher.group(1));
    }
    return Optional.empty();
  }

  private String generateDefaultKey(OutputMarket market) {
    return market.getTemplateMarketName();
  }
}
