package com.ladbrokescoral.oxygen.cms.api.mapping;

import com.ladbrokescoral.oxygen.cms.api.dto.GameDto;
import com.ladbrokescoral.oxygen.cms.api.dto.PrizeDto;
import com.ladbrokescoral.oxygen.cms.api.entity.Game;
import com.ladbrokescoral.oxygen.cms.api.entity.Prize;
import java.util.Collections;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;
import org.mapstruct.factory.Mappers;

@Mapper
public interface GameMapper {
  static GameMapper getInstance() {
    return GameMapperInstance.GAME_MAPPER_INSTANCE;
  }

  @Mapping(target = "prizes", expression = "java(toPrizes(game))")
  GameDto toDto(Game game);

  default Map<Integer, PrizeDto> toPrizes(Game source) {
    List<Prize> prizes = source.getPrizes();
    return prizes != null
        ? prizes.stream()
            .collect(
                Collectors.toMap(
                    Prize::getCorrectSelections,
                    prize ->
                        new PrizeDto()
                            .setPrizeType(prize.getPrizeType())
                            .setAmount(prize.getAmount())))
        : Collections.emptyMap();
  }

  final class GameMapperInstance {
    private static final GameMapper GAME_MAPPER_INSTANCE = Mappers.getMapper(GameMapper.class);

    private GameMapperInstance() {}
  }
}
