package com.oxygen.publisher.sportsfeatured.model;

import static org.junit.Assert.*;

import com.oxygen.publisher.SocketIoTestHelper;
import com.oxygen.publisher.model.PageType;
import com.oxygen.publisher.sportsfeatured.model.module.EventsModule;
import com.oxygen.publisher.sportsfeatured.model.module.QuickLinkModule;
import com.oxygen.publisher.sportsfeatured.model.module.RecentlyPlayedGameModule;
import java.util.HashMap;
import java.util.Objects;
import org.junit.Before;
import org.junit.Test;

public class SportsCachedDataTest {

  private SportsCachedData thisCache;

  @Before
  public void init() {
    thisCache = new SportsCachedData(5, 1);
  }

  @Test
  public void testSportPageMap() {

    thisCache.insertSportPageData(SocketIoTestHelper.getSportPageMapCache());
    assertEquals(6, thisCache.getSportPageData().size());

    thisCache.removeSportIdFromSportPageMapCache("0");
    assertEquals(5, thisCache.getSportPageData().size());
  }

  @Test
  public void testSportPageMapException() {

    thisCache.insertSportPageData(SocketIoTestHelper.getSportPageMapCache());
    assertEquals(6, thisCache.getSportPageData().size());
    // invalid sportId
    thisCache.removeSportIdFromSportPageMapCache("100");
    assertEquals(6, thisCache.getSportPageData().size());
  }

  @Test
  public void testStructureForSportsAreUpdatedIndependently() {
    assertEquals(0, thisCache.getStructureMap().size());

    thisCache.updatePage(createStructure(0, 1));
    thisCache.updatePage(createStructure(1, 0));
    thisCache.updatePage(createStructure(0, 1));
    assertEquals(2, thisCache.getStructureMap().size());
  }

  @Test
  public void mergeForOnePage() {
    assertEquals(String.valueOf(-1), thisCache.getEntityGUID());

    thisCache.updatePage(createStructure(0, 1));
    assertEquals(String.valueOf(1), thisCache.getEntityGUID());
    assertEquals(1, thisCache.getStructureMap().asMap().size());
    assertEquals(3, thisCache.getModuleMap().asMap().size());

    thisCache.updatePage(createStructure(0, 2));
    assertEquals(String.valueOf(2), thisCache.getEntityGUID());
    assertEquals(1, thisCache.getStructureMap().asMap().size());
    assertEquals(3, thisCache.getModuleMap().asMap().size());

    thisCache.updatePage(createStructure(0, 3));
    assertEquals(String.valueOf(3), thisCache.getEntityGUID());
    assertEquals(1, thisCache.getStructureMap().asMap().size());
    assertEquals(3, thisCache.getModuleMap().asMap().size());
  }

  @Test
  public void mergeWithOutDatePageModel() {

    thisCache.updatePage(createStructure(0, 2));
    assertEquals(String.valueOf(2), thisCache.getEntityGUID());

    // should not allow downgrade version for the same sportId
    thisCache.updatePage(createStructure(0, 1));
    assertEquals(String.valueOf(2), thisCache.getEntityGUID());
  }

  @Test
  public void mergeForPluralCase() {

    thisCache.updatePage(createStructure(0, 1));
    thisCache.updatePage(createStructure(1, 1));
    thisCache.updatePage(createStructure(2, 1));

    assertEquals(String.valueOf(1), thisCache.getEntityGUID());
    assertEquals(3, thisCache.getStructureMap().asMap().size());
    assertEquals(9, thisCache.getModuleMap().asMap().size());

    thisCache.updatePage(createStructure(0, 2));
    thisCache.updatePage(createStructure(1, 2));
    thisCache.updatePage(createStructure(2, 2));

    assertEquals(String.valueOf(2), thisCache.getEntityGUID());
    assertEquals(3, thisCache.getStructureMap().asMap().size());
    assertEquals(9, thisCache.getModuleMap().asMap().size());

    thisCache.updatePage(createStructure(0, 3));
    thisCache.updatePage(createStructure(1, 3));
    thisCache.updatePage(createStructure(2, 3));

    assertEquals(String.valueOf(3), thisCache.getEntityGUID());
    assertEquals(3, thisCache.getStructureMap().asMap().size());
    assertEquals(9, thisCache.getModuleMap().asMap().size());
  }

  @Test
  public void isEmptyCheckOk() {
    assertTrue(thisCache.isEmpty());

    thisCache.updatePage(createStructure(555, 555));
    assertFalse(thisCache.isEmpty());
  }

  @Test
  public void generationIsRemovedWithStructureExpiration() {
    assertTrue(thisCache.isEmpty());

    thisCache.updatePage(createStructure(0, 555));
    thisCache.updatePage(createStructure(1, 555));
    thisCache.updatePage(createStructure(2, 555));
    thisCache.updatePage(createStructure(3, 555));
    thisCache.updatePage(createStructure(4, 555));

    assertEquals(5, thisCache.getGenerationMap().size());
    assertTrue(thisCache.getGenerationMap().containsKey(new PageRawIndex(PageType.sport, 0)));

    // further adding, will remove first items
    thisCache.updatePage(createStructure(5, 555));
    assertEquals(5, thisCache.getGenerationMap().size());
    assertEquals(5, thisCache.getStructureMap().size());
    assertFalse(thisCache.getGenerationMap().containsKey(new PageRawIndex(PageType.sport, 0)));
    assertTrue(thisCache.getGenerationMap().containsKey(new PageRawIndex(PageType.sport, 5)));
    assertTrue(
        thisCache.getGenerationMap().keySet().stream()
            .allMatch(k -> Objects.nonNull(thisCache.getStructure(k))));
  }

  private PageCacheUpdate createStructure(int sportId, long version) {
    PageRawIndex.GenerationKey generation =
        PageRawIndex.GenerationKey.fromPage(String.valueOf(sportId), version);
    FeaturedModel featuredModel = new FeaturedModel(String.valueOf(sportId));
    EventsModule evMod = new EventsModule();
    evMod.setId("evn" + sportId);
    evMod.setSportId(sportId);
    QuickLinkModule qlMod = new QuickLinkModule();
    qlMod.setId("ql" + sportId);
    RecentlyPlayedGameModule rpgMod = new RecentlyPlayedGameModule();
    rpgMod.setId("rpg" + sportId);
    rpgMod.setSportId(sportId);
    featuredModel.addModule(evMod);
    featuredModel.addModule(qlMod);
    featuredModel.addModule(rpgMod);

    PageCacheUpdate pageUpdate0 = new PageCacheUpdate(generation);

    assertFalse(pageUpdate0.isFullFill());
    pageUpdate0.setPageModel(featuredModel);
    pageUpdate0.setModuleMap(new HashMap<>());

    pageUpdate0.addModule(evMod);
    pageUpdate0.addModule(qlMod);
    pageUpdate0.addModule(rpgMod); // 3 modules

    pageUpdate0.setPrimaryMarketCache(new HashMap<>());
    assertTrue(pageUpdate0.isFullFill());
    return pageUpdate0;
  }
}
