package com.ladbrokescoral.oxygen.cms.configuration.changelogs.script;

import com.github.cloudyrock.mongock.driver.mongodb.springdata.v3.decorator.impl.MongockTemplate;
import com.ladbrokescoral.oxygen.cms.api.dto.AliasModuleNamesDto;
import com.ladbrokescoral.oxygen.cms.api.entity.RGYModuleEntity;
import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;
import org.apache.commons.collections4.CollectionUtils;
import org.springframework.data.mongodb.core.query.Criteria;
import org.springframework.data.mongodb.core.query.Query;

public class RgyModuleStructureUpdate extends AbstractBrandMongoUpdate {
  private static final String BRAND = "brand";

  private static final String COLLECTION = "rgy-modules";
  private final MongockTemplate mongockTemplate;

  public RgyModuleStructureUpdate(MongockTemplate mongockTemplate) {
    this.mongockTemplate = mongockTemplate;
  }

  public void updateStructureInRgyModules(String brand) {
    Query query = new Query();
    query.addCriteria(Criteria.where(BRAND).is(brand));
    List<RGYModuleEntity> rgyModules =
        this.mongockTemplate.find(query, RGYModuleEntity.class).stream()
            .filter(entity -> entity.getAliasModuleNames() != null)
            .map(this::mapFields)
            .collect(Collectors.toList());
    if (CollectionUtils.isNotEmpty(rgyModules)) {
      rgyModules.forEach((RGYModuleEntity entity) -> this.mongockTemplate.save(entity, COLLECTION));
    }
  }

  private RGYModuleEntity mapFields(RGYModuleEntity entity) {

    List<AliasModuleNamesDto> aliasModules =
        Arrays.stream(entity.getAliasModuleNames().trim().split(","))
            .map(
                (String e) -> {
                  AliasModuleNamesDto dto = new AliasModuleNamesDto();
                  dto.setTitle(e);
                  dto.setAddTag(Boolean.TRUE);
                  return dto;
                })
            .collect(Collectors.toList());
    entity.setAliasModules(aliasModules);
    return entity;
  }
}
