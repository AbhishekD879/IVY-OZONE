package com.ladbrokescoral.oxygen.cms.configuration.changelogs.script;

import com.github.cloudyrock.mongock.driver.mongodb.springdata.v3.decorator.impl.MongockTemplate;
import com.ladbrokescoral.oxygen.cms.api.entity.InplayStatsSorting;
import com.ladbrokescoral.oxygen.cms.configuration.changelogs.DatabaseChangeLog;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.AdditionalAnswers;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.junit.jupiter.MockitoExtension;

@ExtendWith(MockitoExtension.class)
class InplayStatsSortingUpdateTest {

  @Mock private MongockTemplate mongockTemplate;

  private final DatabaseChangeLog databaseChangeLog = new DatabaseChangeLog();

  @Test
  void testInplayStatsSortingInsert() {

    Mockito.when(mongockTemplate.insert(Mockito.any(InplayStatsSorting.class), Mockito.anyString()))
        .thenAnswer(AdditionalAnswers.returnsFirstArg());

    Assertions.assertDoesNotThrow(
        () -> this.databaseChangeLog.addTheInplayStatsSorting(mongockTemplate));
  }
}
