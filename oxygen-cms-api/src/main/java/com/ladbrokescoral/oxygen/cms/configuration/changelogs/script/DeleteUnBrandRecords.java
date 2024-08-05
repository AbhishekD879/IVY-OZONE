package com.ladbrokescoral.oxygen.cms.configuration.changelogs.script;

import com.github.cloudyrock.mongock.driver.mongodb.springdata.v3.decorator.impl.MongockTemplate;
import com.ladbrokescoral.oxygen.cms.api.entity.FooterMenu;
import com.ladbrokescoral.oxygen.cms.api.entity.NavigationPoint;
import java.util.ArrayList;
import java.util.List;
import org.bson.Document;
import org.springframework.data.mongodb.core.query.Criteria;
import org.springframework.data.mongodb.core.query.Query;
import org.springframework.data.mongodb.core.query.Update;

public class DeleteUnBrandRecords {

  private static final String MODULE_COLLECTION_NAME = "segmentedModules";
  private static final String SEGMENT_COLLECTION_NAME = "segments";
  private static final String NAVIGATION_POINTS_COLLECTION_NAME = "navigationPoint";
  private static final String FOOTER_MENU_COLLECTION_NAME = "footermenus";

  /**
   * Segments and SegmentedModules should be specific to Brand level. As we have initially created
   * without Brand specific deleting the collections to cleanup the data. Following ChangeSets take
   * care creating these records at Brand level
   *
   * @param mongockTemplate
   */
  public void deleteUnBrandRecords(MongockTemplate mongockTemplate) {
    boolean cleanUpNeeded = false;
    if (mongockTemplate.collectionExists(MODULE_COLLECTION_NAME)) {
      cleanUpNeeded = true;
      mongockTemplate.dropCollection(MODULE_COLLECTION_NAME);
    }

    if (mongockTemplate.collectionExists(SEGMENT_COLLECTION_NAME)) {
      // Delete the Segments collection
      mongockTemplate.dropCollection(SEGMENT_COLLECTION_NAME);
      cleanUpNeeded = true;
    }
    if (cleanUpNeeded) {
      // Clean up Navigation Points
      List<NavigationPoint> navigationPoints =
          mongockTemplate.findAll(NavigationPoint.class, NAVIGATION_POINTS_COLLECTION_NAME);

      navigationPoints.stream()
          .forEach(
              (NavigationPoint navigationPoint) -> {
                navigationPoint.setSegmentReferences(new ArrayList<>());
                if (!navigationPoint.isUniversalSegment()) {
                  navigationPoint.setUniversalSegment(true);
                  navigationPoint.setInclusionList(new ArrayList<>());
                } else {
                  navigationPoint.setExclusionList(new ArrayList<>());
                }
                Query query = new Query(Criteria.where("_id").is(navigationPoint.getId()));

                Document doc = new Document();
                mongockTemplate.getConverter().write(navigationPoint, doc);
                Update update = Update.fromDocument(doc);

                mongockTemplate.upsert(query, update, NAVIGATION_POINTS_COLLECTION_NAME);
              });

      // Clean up Footer Menu
      List<FooterMenu> footerMenus =
          mongockTemplate.findAll(FooterMenu.class, FOOTER_MENU_COLLECTION_NAME);

      footerMenus.stream()
          .forEach(
              (FooterMenu footerMenu) -> {
                footerMenu.setSegmentReferences(new ArrayList<>());
                if (!footerMenu.isUniversalSegment()) {
                  footerMenu.setUniversalSegment(true);
                  footerMenu.setInclusionList(new ArrayList<>());
                } else {
                  footerMenu.setExclusionList(new ArrayList<>());
                }
                Query query = new Query(Criteria.where("_id").is(footerMenu.getId()));

                Document doc = new Document();
                mongockTemplate.getConverter().write(footerMenu, doc);
                Update update = Update.fromDocument(doc);

                mongockTemplate.upsert(query, update, FOOTER_MENU_COLLECTION_NAME);
              });
    }
  }
}
