package com.ladbrokescoral.oxygen.cms.api.mapping;

import com.ladbrokescoral.oxygen.cms.api.dto.QualificationRuleDto;
import com.ladbrokescoral.oxygen.cms.api.entity.QualificationRule;
import lombok.AccessLevel;
import lombok.NoArgsConstructor;
import org.mapstruct.Mapper;
import org.mapstruct.factory.Mappers;

@Mapper
public interface QualificationRuleMapper {
  static QualificationRuleMapper getInstance() {
    return QualificationRuleMapperSingleton.INSTANCE;
  }

  QualificationRuleDto toDto(QualificationRule entity);

  @NoArgsConstructor(access = AccessLevel.PRIVATE)
  final class QualificationRuleMapperSingleton {
    private static final QualificationRuleMapper INSTANCE =
        Mappers.getMapper(QualificationRuleMapper.class);
  }
}
