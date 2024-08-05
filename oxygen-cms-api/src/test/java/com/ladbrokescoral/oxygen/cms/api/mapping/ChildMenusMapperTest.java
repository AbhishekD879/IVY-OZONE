package com.ladbrokescoral.oxygen.cms.api.mapping;

import static com.ladbrokescoral.oxygen.cms.api.mapping.ChildMenusMapper.extractChildMenus;
import static org.junit.Assert.*;

import com.ladbrokescoral.oxygen.cms.api.entity.HeaderMenu;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;
import org.junit.Test;

public class ChildMenusMapperTest {

  @Test
  public void mappingTest() {
    List<HeaderMenu> headerMenuList = new LinkedList<>();
    headerMenuList.add(createHeaderMenu("1", null, "uno"));
    headerMenuList.add(createHeaderMenu("2", "1", "uno_child_1"));
    headerMenuList.add(createHeaderMenu("3", "4", "dos_child_1"));
    headerMenuList.add(createHeaderMenu("4", "", "dos"));
    headerMenuList.add(createHeaderMenu("5", "1", "uno_child_2"));
    headerMenuList.add(createHeaderMenu("6", null, "tres"));

    Map<String, List<HeaderMenu>> menusMap = extractChildMenus(headerMenuList.stream());
    assertTrue(menusMap.containsKey("1"));
    assertTrue(menusMap.containsKey("4"));
    assertTrue(menusMap.containsKey("6"));
    assertFalse(menusMap.containsKey("2"));
    assertFalse(menusMap.containsKey("3"));
    assertFalse(menusMap.containsKey("5"));
    assertEquals(2, menusMap.get("1").size());
    assertEquals(1, menusMap.get("4").size());
    assertEquals(0, menusMap.get("6").size());
  }

  private HeaderMenu createHeaderMenu(String id, String parentId, String targetUri) {
    HeaderMenu headerMenu = new HeaderMenu();
    headerMenu.setId(id);
    headerMenu.setParent(parentId);
    headerMenu.setTargetUri(targetUri);
    return headerMenu;
  }
}
