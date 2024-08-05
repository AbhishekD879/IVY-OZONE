package com.ladbrokescoral.oxygen.cms.api.mapping;

import com.google.common.collect.Lists;
import com.ladbrokescoral.oxygen.cms.api.dto.BaseMenuDto;
import com.ladbrokescoral.oxygen.cms.api.dto.CountrySettingDto;
import com.ladbrokescoral.oxygen.cms.api.dto.LeftMenuDto;
import com.ladbrokescoral.oxygen.cms.api.dto.SeoSitemapDto;
import com.ladbrokescoral.oxygen.cms.api.entity.Country;
import com.ladbrokescoral.oxygen.cms.api.entity.LeftMenu;
import com.ladbrokescoral.oxygen.cms.api.entity.SeoPage;
import com.ladbrokescoral.oxygen.cms.api.entity.menu.AbstractMenu;
import java.util.Collection;
import java.util.List;
import java.util.Map;
import java.util.Objects;
import java.util.stream.Collectors;
import org.springframework.util.CollectionUtils;
import org.springframework.util.StringUtils;

public class DtoMapper {

  private DtoMapper() {}

  public static LeftMenuDto toDto(LeftMenu entity, List<LeftMenu> childEntities) {
    LeftMenuDto result = new LeftMenuDto();
    if (!CollectionUtils.isEmpty(childEntities)) {
      result.setChildren(childEntities.stream().map(DtoMapper::toDto).collect(Collectors.toList()));
    } else {
      result.setChildren(Lists.newArrayList());
    }
    result.setInApp(entity.getInApp());
    result.setLinkTitle(entity.getLinkTitle());
    result.setShowItemFor(entity.getShowItemFor());
    result.setTargetUri(entity.getTargetUri());

    return result;
  }

  public static List<CountrySettingDto> toDto(Country entity) {

    return entity.getCountriesData().stream()
        .map(
            data ->
                new CountrySettingDto()
                    .setLabel(data.getLabel())
                    .setPhoneAreaCode(data.getPhoneAreaCode())
                    .setVal(data.getVal()))
        .collect(Collectors.toList());
  }

  public static <T extends AbstractMenu> BaseMenuDto toDto(T entity) {

    BaseMenuDto result = new BaseMenuDto();

    result.setLinkTitle(entity.getLinkTitle());
    result.setInApp(entity.getInApp());
    result.setDisabled(entity.getDisabled());
    result.setTargetUri(entity.getTargetUri());

    return result;
  }

  public static Map<String, SeoSitemapDto> toDtoSeoSitemap(Collection<SeoPage> entities) {
    return entities.stream()
        .filter(Objects::nonNull)
        .collect(
            Collectors.toMap(
                SeoPage::getUrl,
                entity ->
                    new SeoSitemapDto()
                        .setChangefreq(entity.getChangefreq())
                        .setPriority(
                            !StringUtils.isEmpty(entity.getPriority())
                                ? entity.getPriority()
                                : null)));
  }
}
