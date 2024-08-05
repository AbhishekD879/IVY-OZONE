package com.ladbrokescoral.oxygen.cms.api.mapping;

import com.ladbrokescoral.oxygen.cms.api.dto.RssRewardDto;
import com.ladbrokescoral.oxygen.cms.api.entity.questionengine.RssReward;
import org.mapstruct.Mapper;
import org.mapstruct.factory.Mappers;
import org.springframework.stereotype.Component;

@Mapper
@Component
public interface RssRewardMapper {
  RssReward toEntity(RssRewardDto entity);

  RssRewardMapper INSTANCE = Mappers.getMapper(RssRewardMapper.class);
}
