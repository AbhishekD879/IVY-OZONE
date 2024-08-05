package com.ladbrokescoral.oxygen.cms.api.mapping;

import com.ladbrokescoral.oxygen.cms.api.dto.ShowOnDto;
import com.ladbrokescoral.oxygen.cms.api.dto.WidgetDto;
import com.ladbrokescoral.oxygen.cms.api.entity.Widget;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import org.mapstruct.AfterMapping;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;
import org.mapstruct.MappingTarget;
import org.springframework.util.CollectionUtils;

@Mapper(uses = WidgetMapUtil.class)
public abstract class WidgetMapper {
  @Mapping(target = "directiveName", source = "widget.type")
  @Mapping(target = "publishedDevices", ignore = true)
  @Mapping(target = "columns", ignore = true)
  @Mapping(
      target = "showOn",
      qualifiedBy = {WidgetMapUtil.WidgetUtils.class, WidgetMapUtil.ShowOn.class})
  public abstract WidgetDto widgetToWidgetDto(Widget widget, List<String> sportCategories);

  @AfterMapping
  protected void setPublishedDevices(Widget widget, @MappingTarget WidgetDto dto) {
    List<String> publishedDevices = new ArrayList<>();
    if (widget.isShowOnDesktop()) publishedDevices.add("desktop");
    if (widget.isShowOnMobile()) publishedDevices.add("mobile");
    if (widget.isShowOnTablet()) publishedDevices.add("tablet");
    dto.setPublishedDevices(publishedDevices);
  }

  @AfterMapping
  protected void setColumns(Widget widget, @MappingTarget WidgetDto dto) {
    dto.setColumns(
        "both".equals(widget.getColumns())
            ? Arrays.asList("rightColumn", "widgetColumn")
            : Arrays.asList(widget.getColumns()));
  }

  @AfterMapping
  protected void setShowOn(
      List<String> sportCategories, Widget widget, @MappingTarget WidgetDto dto) {
    boolean ifExists =
        !CollectionUtils.isEmpty(sportCategories) && widget.getType().equals("match-centre");
    dto.setShowOn(
        ifExists
            ? new ShowOnDto().sports(sportCategories).routes(widget.getShowOn().getRoutes())
            : null);
  }
}
