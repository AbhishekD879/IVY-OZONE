package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.entity.Widget;
import com.ladbrokescoral.oxygen.cms.api.repository.WidgetRepository;
import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

@Component
public class WidgetService extends SortableService<Widget> {
  private final WidgetRepository widgetRepository;

  @Autowired
  public WidgetService(WidgetRepository widgetRepository) {
    super(widgetRepository);
    this.widgetRepository = widgetRepository;
  }

  @Override
  public List<Widget> findAll() {
    return widgetRepository.findAll(SortableService.SORT_BY_SORT_ORDER_ASC);
  }

  public List<Widget> findAllByBrandAndDisabled(String brand) {
    return widgetRepository.findAllByBrandAndDisabledOrderBySortOrderAsc(brand, Boolean.FALSE);
  }

  @Override
  public Widget prepareModelBeforeSave(Widget model) {
    model.setTypeBrand(generateTypeBrand(model));
    return model;
  }

  private String generateTypeBrand(Widget model) {
    return new StringBuilder(model.getType())
        .append("-")
        .append(model.getBrand())
        .toString()
        .toLowerCase()
        .replace(" ", "-");
  }
}
