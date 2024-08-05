package com.coral.oxygen.middleware.in_play.service.model;

import static org.junit.Assert.assertEquals;

import com.coral.oxygen.middleware.in_play.service.TestTools;
import java.util.Collection;
import lombok.extern.slf4j.Slf4j;
import org.junit.Test;

/**
 * To given caches A & B where: A have difference with B in 6 type segments, 3 segments are totally
 * new in A and absent in B, and 3 have an additive count in A.
 *
 * <p>- if we supposed what A is new cache and B previous one, the comparing of the caches will have
 * 3 new and 3 modified type segments.
 *
 * <p>- if we supposed what B is new cache and A previous one, the comparing of the caches will have
 * 3 removed and 0 modified type segments. It supposed what consistency of the model will be covered
 * by live updates in this case.
 *
 * <p>For additional information see BaseObjectBuilder class
 */
@Slf4j
public class CompetitionDifferenceBuilderTest {

  /** added event id = 9995351 */
  @Test
  public void add_case() {
    InPlayCache latestCache =
        TestTools.fromFile(
            "CompetitionDifferenceBuilder/LatastCache_one_new_category_case.json",
            InPlayCache.class);
    InPlayCache previousCache =
        TestTools.fromFile(
            "CompetitionDifferenceBuilder/PreviousCache_one_new_category_case.json",
            InPlayCache.class);
    Collection<SportCompetitionChanges> result =
        CompetitionDifferenceBuilder.builder().compareCaches(latestCache, previousCache).build();

    assertEquals(6, result.size());
    result.stream()
        .peek(
            scc -> {
              assertEquals(0, scc.getRemoved().size());
              if (scc.getAdded().size() > 0) {
                scc.getAdded().values().stream().peek(ts -> assertEquals("442", ts.getTypeId()));
              } else {
                scc.getChanged().stream().peek(typeId -> assertEquals("442", typeId));
              }
            });
  }

  /**
   * added: 0 changed : 0 removed: 3
   *
   * <p>removed event id 9995351
   */
  @Test
  public void remove_case() {
    InPlayCache latestCache =
        TestTools.fromFile(
            "CompetitionDifferenceBuilder/PreviousCache_one_new_category_case.json",
            InPlayCache.class);
    InPlayCache previousCache =
        TestTools.fromFile(
            "CompetitionDifferenceBuilder/LatastCache_one_new_category_case.json",
            InPlayCache.class);
    Collection<SportCompetitionChanges> result =
        CompetitionDifferenceBuilder.builder().compareCaches(latestCache, previousCache).build();

    assertEquals(6, result.size());
    result.stream()
        .peek(
            scc -> {
              assertEquals(0, scc.getAdded().size());
              scc.getRemoved().stream().peek(typeId -> assertEquals("442", typeId));
            });
  }
}
