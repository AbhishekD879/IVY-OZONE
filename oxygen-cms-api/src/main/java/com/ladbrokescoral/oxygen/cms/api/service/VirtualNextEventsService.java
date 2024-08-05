package com.ladbrokescoral.oxygen.cms.api.service;

import com.egalacoral.spark.siteserver.api.SimpleFilter;
import com.egalacoral.spark.siteserver.model.Type;
import com.ladbrokescoral.oxygen.cms.api.dto.ObTypeDto;
import com.ladbrokescoral.oxygen.cms.api.dto.VirtualNextEventDto;
import com.ladbrokescoral.oxygen.cms.api.entity.VirtualNextEvent;
import com.ladbrokescoral.oxygen.cms.api.mapping.VirtualNextEventsMapper;
import com.ladbrokescoral.oxygen.cms.api.repository.VirtualNextEventsRepository;
import com.ladbrokescoral.oxygen.cms.api.service.siteserve.SiteServeApiProvider;
import java.util.Arrays;
import java.util.Collection;
import java.util.Collections;
import java.util.List;
import java.util.function.Predicate;
import java.util.stream.Collectors;
import org.apache.commons.collections4.CollectionUtils;
import org.springframework.cache.annotation.Cacheable;
import org.springframework.stereotype.Service;

@Service
public class VirtualNextEventsService extends SortableService<VirtualNextEvent> {

  private final SiteServeApiProvider siteServeApiProvider;

  public VirtualNextEventsService(
      VirtualNextEventsRepository repository, SiteServeApiProvider siteServeApiProvider) {
    super(repository);
    this.siteServeApiProvider = siteServeApiProvider;
  }

  public List<VirtualNextEventDto> readByBrandAndActive(String brand) {

    Predicate<VirtualNextEvent> predicate = entity -> (!entity.isDisabled());

    return this.repository.findByBrand(brand).stream()
        .filter(predicate)
        .map(VirtualNextEventsMapper.MAPPER::toDto)
        .collect(Collectors.toList());
  }

  @Cacheable(value = "virtual-next-events", key = "#brand+ '_' +#classId")
  public List<ObTypeDto> getOBTypesForClass(String brand, String classId) {
    String[] classIds = classId.trim().split(",");

    List<String> classes = Arrays.stream(classIds).map(String::trim).collect(Collectors.toList());

    return this.siteServeApiProvider
        .api(brand)
        .getClassToSubTypeForClass(
            classes, (SimpleFilter) new SimpleFilter.SimpleFilterBuilder().build())
        .filter(CollectionUtils::isNotEmpty)
        .map(Collection::stream)
        .map(typeStream -> typeStream.map(this::mapToObTypeDto).collect(Collectors.toList()))
        .orElse(Collections.emptyList());
  }

  private ObTypeDto mapToObTypeDto(Type type) {
    ObTypeDto obTypeDto = new ObTypeDto();
    obTypeDto.setTypeId(type.getId());
    obTypeDto.setTypeName(buildTypeName(type.getName()));
    return obTypeDto;
  }

  private String buildTypeName(String typeName) {
    return typeName.replace("|", "").trim();
  }
}
