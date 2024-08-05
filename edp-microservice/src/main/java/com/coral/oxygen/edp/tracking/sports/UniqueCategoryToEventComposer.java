package com.coral.oxygen.edp.tracking.sports;

import com.coral.oxygen.edp.model.output.OutputEvent;
import com.coral.oxygen.edp.tracking.model.CategoryToUpcomingEvent;
import com.egalacoral.spark.siteserver.model.Category;
import java.util.ArrayList;
import java.util.Collection;
import java.util.Collections;
import java.util.Comparator;
import java.util.List;
import java.util.Map;
import java.util.TreeSet;
import java.util.stream.Collectors;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Component;
import org.springframework.util.CollectionUtils;

/**
 * Composes list of {@link CategoryToUpcomingEvent} where only unique categories exists. If there
 * was two or more events for category, only one with lowest displayOrder will be selected
 *
 * <p>NOTE: SiteServer Category object really corresponds to OpenBet's Class.
 */
@Component
@Slf4j
public class UniqueCategoryToEventComposer implements CategoryToUpcomingEventComposer {

  @Override
  public List<CategoryToUpcomingEvent> composeCategoriesToEvents(
      Collection<? extends Category> categories, Collection<? extends OutputEvent> events) {
    if (CollectionUtils.isEmpty(categories) || CollectionUtils.isEmpty(events)) {
      return Collections.emptyList();
    } else {
      Collection<Category> uniqueCategories = getOnlyUniqueCategories(categories);

      Map<Integer, List<OutputEvent>> groupByClassId =
          groupEventsByClassIdAndSortByDispOrder(events);

      List<CategoryToUpcomingEvent> result = new ArrayList<>();

      for (Category category : uniqueCategories) {
        Integer classId = category.getId();
        groupByClassId.getOrDefault(classId, Collections.emptyList()).stream()
            .findFirst()
            .map(event -> new CategoryToUpcomingEvent(event, category))
            .ifPresent(result::add);
      }
      return result;
    }
  }

  private Map<Integer, List<OutputEvent>> groupEventsByClassIdAndSortByDispOrder(
      Collection<? extends OutputEvent> events) {
    return events.stream()
        .sorted(Comparator.comparing(OutputEvent::getDisplayOrder))
        .collect(Collectors.groupingBy(e -> Integer.parseInt(e.getClassId())));
  }

  private Collection<Category> getOnlyUniqueCategories(Collection<? extends Category> categories) {
    Collection<Category> uniqueCategories = new TreeSet<>(Comparator.comparing(Category::getId));
    uniqueCategories.addAll(categories);
    return uniqueCategories;
  }
}
