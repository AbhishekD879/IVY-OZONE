package com.ladbrokescoral.oxygen.cms.api.service.public_api;

import com.ladbrokescoral.oxygen.cms.api.dto.WidgetDto;
import com.ladbrokescoral.oxygen.cms.api.entity.SportCategory;
import com.ladbrokescoral.oxygen.cms.api.entity.Widget;
import com.ladbrokescoral.oxygen.cms.api.mapping.WidgetMapper;
import com.ladbrokescoral.oxygen.cms.api.repository.SportCategoryRepository;
import com.ladbrokescoral.oxygen.cms.api.service.BybTabAvailabilityService;
import com.ladbrokescoral.oxygen.cms.api.service.WidgetService;
import java.util.ArrayList;
import java.util.Collection;
import java.util.List;
import java.util.Map;
import java.util.Objects;
import java.util.stream.Collectors;
import lombok.RequiredArgsConstructor;
import org.mapstruct.factory.Mappers;
import org.springframework.stereotype.Service;
import org.springframework.util.CollectionUtils;

@Service
@RequiredArgsConstructor
public class WidgetPublicService {
  private static final String BUILD_YOUR_BET_TYPE = "build-your-bet";

  private final WidgetService service;
  private final SportCategoryRepository sportCategoryRepository;
  private final BybTabAvailabilityService bybTabAvailabilityService;

  public List<WidgetDto> findByBrand(String brand) {

    WidgetMapper mapper = Mappers.getMapper(WidgetMapper.class);

    List<Widget> widgetCollection = service.findAllByBrandAndDisabled(brand);
    Map<String, List<String>> sportCategories = getSportCategories(widgetCollection);

    for (Map.Entry<String, List<String>> entry : sportCategories.entrySet()) {
      List<String> sportTargetUris =
          sportCategoryRepository.findAllByMatchingIds(entry.getValue()).stream()
              .map(SportCategory::getTargetUri)
              .collect(Collectors.toList());
      entry.setValue(sportTargetUris);
    }

    List<WidgetDto> result = new ArrayList<>();
    for (Widget widget : widgetCollection) {
      if (widget.getType().equals(BUILD_YOUR_BET_TYPE)
          && !bybTabAvailabilityService.isBybEnabledAndLeaguesAvailable(brand)) {
        continue;
      }

      result.add(mapper.widgetToWidgetDto(widget, sportCategories.get(widget.getId())));
    }

    return result;
  }

  private Map<String, List<String>> getSportCategories(Collection<Widget> widgets) {
    return widgets.stream()
        .filter(
            widget ->
                Objects.nonNull(widget.getShowOn())
                    && !CollectionUtils.isEmpty(widget.getShowOn().getSports()))
        .collect(Collectors.toMap(Widget::getId, widget -> widget.getShowOn().getSports()));
  }
}
