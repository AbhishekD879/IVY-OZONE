package com.ladbrokescoral.oxygen.cms.api.mapping;

import com.google.common.collect.Sets;
import com.ladbrokescoral.oxygen.cms.api.dto.SiteServeEventTreeNodeDto;
import com.ladbrokescoral.oxygen.cms.api.entity.StreamAndBetShortNode;
import java.util.*;
import java.util.function.Function;
import java.util.stream.Collectors;
import java.util.stream.Stream;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Component;

@Slf4j
@Component
public class EventTreeMapper {
  /**
   * method generates next kind of map:
   *
   * <p>categoryId_0: [list of it`s classes] ... categoryId_N: [...] ... classId_0: [list of it`s
   * types] ... classId_N: [...] ... typeId_0: [list of it`s events] ... typeId_N: [...] ... this
   * map is used for validation purposes (dropdowns in UI StreamAndBet)
   *
   * @param nodeList
   * @return
   */
  public Map<String, Set<StreamAndBetShortNode>> toDtoMap(
      List<SiteServeEventTreeNodeDto> nodeList) {
    Map<String, Set<StreamAndBetShortNode>> nodes =
        nodeList.stream()
            .reduce(
                new HashMap<>(),
                (map, node) -> {
                  this.populateMap(node, map);
                  return map;
                },
                EventTreeMapper::combineMaps);
    nodes.forEach(
        (key, value) -> {
          Set<StreamAndBetShortNode> sorted =
              value.stream()
                  .sorted(Comparator.comparing(StreamAndBetShortNode::getName))
                  .collect(Collectors.toCollection(LinkedHashSet::new));
          nodes.put(key, sorted);
        });
    return nodes;
  }

  private void populateMap(
      SiteServeEventTreeNodeDto node, Map<String, Set<StreamAndBetShortNode>> map) {
    map.computeIfPresent(
        node.getCategoryId(),
        (key, classes) -> {
          classes.add(getClassMapper().apply(node));
          return classes;
        });
    map.computeIfPresent(
        node.getClassId(),
        (key, types) -> {
          types.add(getTypeMapper().apply(node));
          return types;
        });
    map.computeIfPresent(
        node.getTypeId(),
        (key, events) -> {
          events.add(getEventMapper().apply(node));
          return events;
        });

    map.putIfAbsent(node.getTypeId(), Sets.newHashSet(getEventMapper().apply(node)));
    map.putIfAbsent(node.getClassId(), Sets.newHashSet(getTypeMapper().apply(node)));
    map.putIfAbsent(node.getCategoryId(), Sets.newHashSet(getClassMapper().apply(node)));
  }

  private Function<SiteServeEventTreeNodeDto, StreamAndBetShortNode> getClassMapper() {
    return StreamAndBetMapper.INSTANCE::toClassDto;
  }

  private Function<SiteServeEventTreeNodeDto, StreamAndBetShortNode> getTypeMapper() {
    return StreamAndBetMapper.INSTANCE::toTypeDto;
  }

  private Function<SiteServeEventTreeNodeDto, StreamAndBetShortNode> getEventMapper() {
    return StreamAndBetMapper.INSTANCE::toEventDto;
  }

  private static HashMap<String, Set<StreamAndBetShortNode>> combineMaps(
      HashMap<String, Set<StreamAndBetShortNode>> map0,
      HashMap<String, Set<StreamAndBetShortNode>> map1) {
    return new HashMap<>(
        Stream.concat(map0.entrySet().stream(), map1.entrySet().stream())
            .collect(
                Collectors.toMap(
                    Map.Entry::getKey,
                    Map.Entry::getValue,
                    (list0, list1) ->
                        Stream.of(list0, list1).flatMap(Set::stream).collect(Collectors.toSet()))));
  }
}
