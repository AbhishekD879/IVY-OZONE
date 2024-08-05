package com.ladbrokescoral.oxygen.cms.api.mapping;

import com.ladbrokescoral.oxygen.cms.api.entity.menu.AbstractMenu;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;
import java.util.Map.Entry;
import java.util.stream.Collectors;
import java.util.stream.Stream;
import org.springframework.util.StringUtils;

public class ChildMenusMapper {

  private ChildMenusMapper() {}

  public static <T extends AbstractMenu> Map<String, List<T>> extractChildMenus(
      Stream<T> menuStream) {
    return menuStream.reduce(
        new HashMap<String, List<T>>(),
        (map, headerMenu) -> {
          if (!StringUtils.isEmpty(headerMenu.getParent())) {
            if (!map.containsKey(headerMenu.getParent())) {
              List<T> newChildList = new LinkedList<>();
              newChildList.add(headerMenu);
              map.put(headerMenu.getParent(), newChildList);
            } else {
              map.get(headerMenu.getParent()).add(headerMenu);
            }
          } else if (!map.containsKey(headerMenu.getId())) {
            map.put(headerMenu.getId(), new ArrayList<>());
          }
          return map;
        },
        // in case of parallel processing next combiner will merge map pairs
        (map0, map1) ->
            new HashMap<>(
                Stream.concat(map0.entrySet().stream(), map1.entrySet().stream())
                    .collect(
                        Collectors.toMap(
                            Entry::getKey,
                            Entry::getValue,
                            (list0, list1) ->
                                Stream.of(list0, list1)
                                    .flatMap(List::stream)
                                    .collect(Collectors.toList())))));
  }
}
