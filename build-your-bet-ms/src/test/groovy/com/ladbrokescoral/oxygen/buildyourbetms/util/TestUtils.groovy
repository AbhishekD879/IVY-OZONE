package com.ladbrokescoral.oxygen.buildyourbetms.util

import com.ladbrokescoral.oxygen.byb.banach.dto.external.GetLeaguesResponseDto

class TestUtils {
  public static List<GetLeaguesResponseDto> createLeagues(long ... ids) {
    return ids.collect {
      GetLeaguesResponseDto.builder().obTypeId(it).build()
    }
  }
}
