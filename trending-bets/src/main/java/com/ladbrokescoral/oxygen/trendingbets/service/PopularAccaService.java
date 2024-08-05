package com.ladbrokescoral.oxygen.trendingbets.service;

import com.ladbrokescoral.oxygen.trendingbets.context.PopularAccaContext;
import com.ladbrokescoral.oxygen.trendingbets.dto.PopularAccaDto;
import com.ladbrokescoral.oxygen.trendingbets.dto.PopularAccaResponse;
import com.ladbrokescoral.oxygen.trendingbets.dto.PopularAccaType;
import com.ladbrokescoral.oxygen.trendingbets.model.TrendingPosition;
import java.util.*;
import java.util.function.BiPredicate;
import java.util.function.Function;
import java.util.stream.Collectors;
import java.util.stream.Stream;
import org.apache.commons.lang3.BooleanUtils;
import org.jetbrains.annotations.NotNull;
import org.springframework.stereotype.Service;
import org.springframework.util.CollectionUtils;

@Service
public class PopularAccaService {

  public PopularAccaResponse processRequest(PopularAccaDto popularAccaDto) {

    Stream<TrendingPosition> trendingPositionStream =
        getTrendingBetsByType(popularAccaDto.getKey(), popularAccaDto.getValues());
    return getPopularAccaResponse(popularAccaDto, trendingPositionStream);
  }

  private Stream<TrendingPosition> getTrendingBetsByType(PopularAccaType key, List<String> values) {
    if (PopularAccaType.SELECTION.equals(key)) {

      return values.stream().map(PopularAccaContext.getSelectionAccas()::get);

    } else if (PopularAccaType.EVENT.equals(key)) {

      return values.stream()
          .flatMap(
              value ->
                  PopularAccaContext.getEventAccas()
                      .getOrDefault(value, Collections.emptySet())
                      .stream());

    } else if (PopularAccaType.TYPEID.equals(key)) {
      return values.stream()
          .flatMap(
              value ->
                  PopularAccaContext.getLeagueAccas()
                      .getOrDefault(value, Collections.emptySet())
                      .stream());

    } else {
      return PopularAccaContext.getSelectionAccas().values().stream();
    }
  }

  private PopularAccaResponse getPopularAccaResponse(
      PopularAccaDto request, Stream<TrendingPosition> eventStream) {
    List<TrendingPosition> positions = computePopularAccas(eventStream, request);

    return PopularAccaResponse.builder()
        .positions(positions.size() >= request.getMinAccas() ? positions : Collections.emptyList())
        .build();
  }

  private List<TrendingPosition> computePopularAccas(
      Stream<TrendingPosition> trendingPositions, PopularAccaDto request) {

    return filterTrendingPositions(trendingPositions, request)
        .collect(
            Collectors.toMap(
                (TrendingPosition position) -> position.getEvent().getId(),
                Function.identity(),
                (TrendingPosition p1, TrendingPosition p2) ->
                    p1.getNBets() > p2.getNBets() ? p1 : p2))
        .values()
        .stream()
        .sorted(Comparator.comparingInt(TrendingPosition::getNBets).reversed())
        .limit(request.getMaxAccas())
        .collect(Collectors.toCollection(ArrayList::new));
  }

  private Stream<TrendingPosition> filterTrendingPositions(
      Stream<TrendingPosition> trendingPositions, PopularAccaDto request) {
    return trendingPositions
        .parallel()
        .filter(Objects::nonNull)
        .filter(tp -> BooleanUtils.isNotTrue(tp.getEvent().getIsSuspended()))
        .filter(tp -> BooleanUtils.isNotTrue(tp.getEvent().getEventIsLive()))
        .filter(tp -> checkThresholdValue().test(tp, request.getThresholdValue()))
        .filter(tp -> checkMarketIdentifier().test(tp, request.getMarketIdentifiers()));
  }

  @NotNull
  private BiPredicate<TrendingPosition, Integer> checkThresholdValue() {
    return (tp, threshold) -> threshold == 0 || threshold < tp.getNBets();
  }

  @NotNull
  private BiPredicate<TrendingPosition, List<String>> checkMarketIdentifier() {
    return (tp, marketIdentifier) ->
        CollectionUtils.isEmpty(marketIdentifier)
            || marketIdentifier.contains(tp.getEvent().getMarkets().get(0).getTemplateMarketName());
  }
}
