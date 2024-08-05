package com.ladbrokescoral.oxygen.cms.configuration.changelogs.script;

import com.github.cloudyrock.mongock.driver.mongodb.springdata.v3.decorator.impl.MongockTemplate;
import com.ladbrokescoral.oxygen.cms.api.dto.InplayStatsSortingDto;
import com.ladbrokescoral.oxygen.cms.api.mapping.InplayStatsSortingMapper;
import java.util.Arrays;
import java.util.List;
import java.util.concurrent.atomic.AtomicInteger;

public class InplayStatsSortingUpdate extends AbstractBrandMongoUpdate {

  private static final String COLLECTION_NAME = "inplay-stats-sorting";

  private static final int FOOTBALL_ID = 16;

  private static final int SORT_ORDER_INIT = 10;
  private final MongockTemplate mongockTemplate;

  public InplayStatsSortingUpdate(MongockTemplate mongockTemplate) {
    this.mongockTemplate = mongockTemplate;
  }

  public void insertStats(String brand) {
    List<String> stats =
        Arrays.asList(
            "Competition,Competition",
            "Stat-Total,Total Stats",
            "Stat-Team Difference,Difference Stats",
            "Primary Odds,Home Odds",
            "Secondary Odds,Away Odds",
            "Match Time, Match Time");
    AtomicInteger sortOrder = new AtomicInteger(SORT_ORDER_INIT);
    stats.forEach(
        (String data) -> saveStats(brand, FOOTBALL_ID, data, sortOrder.getAndIncrement()));
  }

  private void saveStats(String brand, Integer categoryId, String data, int sortOrder) {
    String[] lableAndKey = data.trim().split(",");
    InplayStatsSortingDto dto = new InplayStatsSortingDto();
    dto.setBrand(brand);
    dto.setCategoryId(categoryId);
    dto.setLabel(lableAndKey[0]);
    dto.setReferenceKey(lableAndKey[1]);
    dto.setEnabled(true);
    dto.setSortOrder((double) sortOrder);
    this.mongockTemplate.insert(InplayStatsSortingMapper.MAPPER.toEntity(dto), COLLECTION_NAME);
  }
}
