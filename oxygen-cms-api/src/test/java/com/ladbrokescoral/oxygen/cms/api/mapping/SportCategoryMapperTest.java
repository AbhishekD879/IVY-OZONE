package com.ladbrokescoral.oxygen.cms.api.mapping;

import com.ladbrokescoral.oxygen.cms.api.dto.SportCategoryDto;
import com.ladbrokescoral.oxygen.cms.api.entity.OddsCardHeaderType;
import com.ladbrokescoral.oxygen.cms.api.entity.SportCategory;
import org.junit.Assert;
import org.junit.Test;
import org.mapstruct.factory.Mappers;

public class SportCategoryMapperTest {

  SportCategoryMapper INSTANCE = Mappers.getMapper(SportCategoryMapper.class);

  @Test
  public void categoryShouldContainsConfig() {

    SportCategory sportCategory = new SportCategory();
    sportCategory.setImageTitle("imtitle");
    sportCategory.setTargetUri("public/1/football test");
    sportCategory.setDispSortNames("test sort");
    sportCategory.setOutrightSport(false);
    sportCategory.setOddsCardHeaderType(OddsCardHeaderType.ONE_TWO_TYPE);
    SportCategoryDto dto = INSTANCE.toDto(sportCategory);

    Assert.assertNotNull(dto.getSportConfig());
    Assert.assertNotNull(dto.getSportConfig().getConfig());
    Assert.assertNotNull(dto.getSportConfig().getConfig().getOddsCardHeaderType());
    Assert.assertEquals("oneTwoType", dto.getSportConfig().getConfig().getOddsCardHeaderType());
    Assert.assertEquals("footballtest", dto.getSportConfig().getConfig().getName());
    Assert.assertEquals("football test", dto.getSportConfig().getConfig().getPath());
    Assert.assertArrayEquals(
        new String[] {"test", "sort"},
        dto.getSportConfig().getConfig().getRequest().getDispSortName());

    Assert.assertNotNull(dto.getSportConfig().getConfig().getRequest());
    Assert.assertNotNull(dto.getSportConfig().getConfig().getRequest().getMarketsCount());
  }

  @Test
  public void horseRacingNameMustBeEmpty() {
    SportCategory sportCategory = new SportCategory();
    sportCategory.setTargetUri("horse-racing");
    SportCategoryDto dto = INSTANCE.toDto(sportCategory);

    Assert.assertEquals("horseracing", dto.getSportConfig().getConfig().getName());
  }
}
